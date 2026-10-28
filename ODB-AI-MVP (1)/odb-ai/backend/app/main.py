import os
from datetime import datetime, timezone
from typing import Literal

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, String, Float, DateTime, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, Session

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./odb_ai.db")
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass

class Workload(Base):
    __tablename__ = "workloads"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), index=True)
    description: Mapped[str] = mapped_column(String(3000))
    profile: Mapped[str] = mapped_column(String(120))
    estimated_monthly_usd: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(30), default="draft")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ODB AI API", version="0.1.0",
              description="Prototype API. Add authentication and tenant authorization before deployment.")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class WorkloadCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: str = Field(min_length=1, max_length=3000)
    profile: str = Field(min_length=1, max_length=120)
    estimated_monthly_usd: float = Field(ge=0, le=100_000_000)

class WorkloadOut(BaseModel):
    id: int
    name: str
    description: str
    profile: str
    estimated_monthly_usd: float
    status: str
    created_at: datetime
    model_config = {"from_attributes": True}

class EstimateRequest(BaseModel):
    compute_hours: float = Field(ge=0, le=744)
    compute_hourly_usd: float = Field(ge=0, le=100_000)
    model_calls: int = Field(ge=0, le=10_000_000_000)
    model_cost_per_1000_calls_usd: float = Field(ge=0, le=1_000_000)
    storage_gb: float = Field(ge=0, le=10_000_000)
    storage_usd_per_gb_month: float = Field(ge=0, le=100_000)

@app.get("/health")
def health():
    return {"status": "ok", "environment": "prototype", "live_cloud": False}

@app.get("/api/v1/workloads", response_model=list[WorkloadOut])
def list_workloads(db: Session = Depends(get_db)):
    return list(db.scalars(select(Workload).order_by(Workload.id.desc())).all())

@app.post("/api/v1/workloads", response_model=WorkloadOut, status_code=201)
def create_workload(payload: WorkloadCreate, db: Session = Depends(get_db)):
    item = Workload(**payload.model_dump(), status="draft")
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@app.post("/api/v1/estimate")
def estimate(payload: EstimateRequest):
    compute = payload.compute_hours * payload.compute_hourly_usd
    model = payload.model_calls / 1000 * payload.model_cost_per_1000_calls_usd
    storage = payload.storage_gb * payload.storage_usd_per_gb_month
    subtotal = compute + model + storage
    return {
        "estimate_type": "illustrative",
        "currency": "USD",
        "components": {
            "compute": round(compute, 4),
            "model_api": round(model, 4),
            "storage": round(storage, 4),
        },
        "subtotal": round(subtotal, 4),
        "omissions": ["network transfer", "tax", "discounts", "database", "monitoring", "provider-specific fees"],
        "note": "Uses caller-supplied rates. Not a live provider quote or invoice."
    }
