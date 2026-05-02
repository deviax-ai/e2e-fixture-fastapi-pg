# notes-fastapi-pg

Tiny notes API. FastAPI + SQLAlchemy 2.0 + Alembic + Postgres.
Two endpoints: `GET /notes` and `POST /notes`.

## Run locally

```sh
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# requires a Postgres at localhost:5432 with db=notes user=postgres
alembic upgrade head
uvicorn app.main:app --reload
```

## Why this fixture exists

Phase 1 most-painful-pillar of the
[Deviax](https://github.com/deviax-ai/aura_deploy) E2E fixture matrix.

Exercises the **managed-deps + migrations** path: pipeline must
provision a Postgres, surface DATABASE_URL via env, run
`alembic upgrade head` before the first request, and produce a
multi-stage Dockerfile that drops to non-root.

## Seeded "vibe-problems"

| File | Line | What's wrong |
|---|---|---|
| `app/db.py` | 11 | `DATABASE_URL` hardcoded to `localhost:5432`. |
| `app/main.py` | 18 | `SECRET_KEY` hardcoded. |
| `alembic.ini` | 9 | `sqlalchemy.url` hardcoded — alembic offline mode reads this. |
| `Dockerfile` | 7 | `python:3.9` is EOL; no `USER`, no `HEALTHCHECK`, no `alembic upgrade head`. |
| `app/main.py` | 41 | No `/healthz` route — k8s readinessProbe has nothing to hit. |

`expected.json` declares:

```jsonc
"assert": {
  "outcome": "success",
  "url_status_class": "2xx",
  "url_status_after_1h": "not_5xx"
}
```

## License

MIT.
