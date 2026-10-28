# ODB AI — AI infrastructure planning MVP

ODB AI helps early-stage teams plan AI workloads, inspect illustrative costs, and keep workload definitions organized. This repository contains a responsive interactive demo and a starter API.

## What works in this MVP

- Responsive marketing-style application shell and navigation.
- Interactive workload planning flow with input validation.
- Transparent rule-based compute profile suggestions and illustrative cost estimate.
- Editable cost calculator with compute, model API, and storage assumptions.
- Session-only workload definition creation, search, removal, and JSON export.
- Clear demo labels; no fake live metrics, connected clouds, model inferences, invoices, or deployments.
- FastAPI backend scaffold with health, workload create/list, estimate endpoint, and SQLAlchemy persistence when PostgreSQL is configured.
- Basic API test.

## Product problem and positioning

AI teams report cost and integration friction. DigitalOcean's February 2026 survey of 1,100+ developers, CTOs, and founders reported 49% citing high inference costs as a top scaling challenge. Among teams using multiple tools, common issues included separate tools/APIs (50%), cost predictability (49%), and deployment/orchestration complexity (48%). These are survey findings, not universal population statistics.

ODB AI positioning: **Plan smarter. Build with confidence.**

## Run the frontend

Option A: open `frontend/index.html` in a browser.  
Option B: run a static server:

```bash
cd frontend
python -m http.server 5173
```

Visit `http://localhost:5173`.

## Run the API

Requires Python 3.11+ recommended.

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API docs: `http://127.0.0.1:8000/docs`

Default local mode uses SQLite at `backend/odb_ai.db` for convenience. Set `DATABASE_URL` to a PostgreSQL connection string for a persistent shared environment, e.g.:

```text
DATABASE_URL=postgresql+psycopg://odb_user:replace_me@localhost:5432/odb_ai
```

Set it in your shell/deployment secret configuration. Never commit production secrets.

## API endpoints

- `GET /health`
- `GET /api/v1/workloads`
- `POST /api/v1/workloads`
- `POST /api/v1/estimate`

The starter API is unauthenticated for local development. **Do not expose it publicly as-is.** Before multi-user production use, add a trusted auth integration, verify JWTs server-side, authorize organization/workspace ownership on every object, use migrations, rate limits, structured logs, secret management, and security tests.

## Demo calculator assumptions

Planner rate presets are illustrative flat estimates and are not quotes. Cost calculator uses:

`compute hours × compute hourly rate + (model API calls ÷ 1,000 × model unit cost) + storage GB × storage monthly rate`

Network transfer, database services, load balancers, observability, taxes, minimums, discounts, reserved commitments, and provider-specific metering are omitted. Model call pricing is a user-supplied hypothetical unit price, not token-based live pricing.

## Production roadmap

1. **Foundation:** auth, organization tenancy, PostgreSQL migrations, audit events, secrets and permission model.
2. **Verified cost data:** provider price catalog with timestamps, region/instance assumptions, and billing export ingestion.
3. **AI assistant:** secure server-side model adapter, schema-validated outputs, guardrails, and traceable rationale.
4. **Execution:** provider adapters using least-privilege credentials; deployment approval, idempotency, rollback and logs.
5. **Cost intelligence:** metered usage import, budget notifications, forecasting evaluation and recommendation feedback.
6. **Commercial:** user research, pricing validation, billing provider, terms/privacy and customer support.

## Cloud-credit application readiness

Do not claim eligibility or credit approval. Confirm each program's current requirements directly. Prepare:
- Company formation and ownership evidence where relevant.
- Product demo, roadmap and technical architecture.
- Verified founder/cofounder roles and technical ownership.
- Genuine customer interviews, waitlist or pilot evidence.
- Cloud forecast with assumptions and actual metering separated.
- Data protection and security plan.
- Supporting documents for any eligibility criteria claimed.

## Architecture (target state)

Browser app → authenticated API → organization authorization → workload planner/model adapter → provider adapter → cloud account. PostgreSQL stores workspace metadata and workload definitions; secrets stay in managed secret storage. Cloud operations should require scoped identity, explicit user authorization and auditable actions.

Current delivered demo does not implement that production topology end-to-end.
