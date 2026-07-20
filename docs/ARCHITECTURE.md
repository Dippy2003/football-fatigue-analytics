# PlayerPulse architecture

## Day 1 system context

```mermaid
flowchart LR
    Reviewer[Coach, analyst, or reviewer] --> Web[React + TypeScript web client]
    Web -->|JSON over /api/v1| API[FastAPI modular monolith]
    API --> ORM[SQLAlchemy session layer]
    ORM --> SQLite[(SQLite local fallback)]
    ORM -. production configuration .-> PostgreSQL[(PostgreSQL)]
```

The frontend and backend are independently runnable and testable. The backend
will own data validation, analytics, persistence, and risk explanations. The
browser will receive bounded typed summaries rather than raw tracking frames.

## Current request flow

```text
Browser request
→ React Router page
→ typed Axios client (available for data-driven pages)
→ /api/v1 FastAPI route
→ Pydantic response model
→ JSON response
→ TanStack Query cache (foundation configured)
→ accessible UI state
```

At Day 1 only the system routes return data. Placeholder frontend routes do not
invent match, player, analytics, or risk content.

## Backend modules

- `app/main.py`: application factory, CORS middleware, logging, route assembly.
- `app/core/`: typed settings and safe structured logging.
- `app/api/routes/system.py`: liveness, readiness, and version contracts.
- `app/db/`: engine/session lifecycle and shared UUID/UTC model base.
- `alembic/`: database migration environment.

Future analytics remain modules in the same backend process. This modular
monolith keeps transactions and tests simple while allowing clean boundaries.

## Frontend modules

- `app/`: route configuration and global providers.
- `components/layout/`: original brand mark and responsive shell.
- `pages/`: landing, accessible placeholders, and not-found state.
- `services/api/`: isolated Axios client and typed system calls.
- `types/`: API response contracts.
- `test/`: browser-like jsdom setup.

## Deployment shape

```mermaid
flowchart TB
    Static[Static frontend host] --> Container[FastAPI container]
    Container --> ManagedDB[(Managed PostgreSQL)]
    Container -. temporary cache only .-> Disk[Ephemeral local disk]
```

The planned public deployment regenerates synthetic demo data and stores
durable summaries in PostgreSQL. It cannot depend on persistent local disk and
will keep third-party uploads disabled by default.
