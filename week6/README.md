# Week 6

Minimal full‑stack starter for experimenting with autonomous coding agents.

- FastAPI backend with SQLite (SQLAlchemy)
- Static frontend (no Node toolchain needed)
- Minimal tests (pytest)
- Pre-commit (black + ruff)
- Tasks to practice agent-driven workflows

## Quickstart

1) Create and activate a virtualenv, then install dependencies

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .[dev]
```

2) Run the app (from `week6/`)

```bash
cd week6 && make run
```

Open `http://localhost:8000` for the frontend and `http://localhost:8000/docs` for the API docs.

## Structure

```
backend/                # FastAPI app
frontend/               # Static UI served by FastAPI
data/                   # SQLite DB + seed
docs/                   # TASKS for agent-driven workflows
```

## Tests

```bash
cd week6 && make test
```

## Formatting/Linting

```bash
cd week6 && make format
cd week6 && make lint
```

## Configuration

Copy `.env.example` to `.env` (in `week6/`) to override defaults like the database path.
