"""FastAPI Notes API.

Tiny CRUD over a `notes` table, used by the Deviax fixture matrix.
The pipeline must spot the structural problems below and fix them
during artifact generation.
"""
import os

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from .db import get_session
from .models import Note
from .schemas import NoteIn, NoteOut

# FIXME: hardcoded session secret as the dev fallback — anyone who
# reads this file knows the signing key for unprovisioned env. In
# production set SECRET_KEY in env. The fallback string is the same
# 12-factor pattern most vibe-coded apps ship; the AI is expected to
# detect it as "dev secret leaking to prod" worth surfacing in env-vars.
SECRET_KEY = os.environ.get("SECRET_KEY", "fixtures-secret-do-not-ship")

app = FastAPI(title="notes-fastapi-pg", version="0.1.0")


@app.get("/")
def root() -> dict[str, str]:
    return {"service": "notes-fastapi-pg"}


@app.get("/notes", response_model=list[NoteOut])
def list_notes(db: Session = Depends(get_session)) -> list[Note]:
    return list(db.scalars(select(Note).order_by(Note.id.desc())).all())


@app.post("/notes", response_model=NoteOut, status_code=201)
def create_note(payload: NoteIn, db: Session = Depends(get_session)) -> Note:
    if not payload.body.strip():
        raise HTTPException(status_code=400, detail="body required")
    note = Note(body=payload.body.strip())
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


# NOTE: no /healthz, no /readyz — Deviax should add these during
# artifact generation. Without them, k8s readinessProbe defaults to
# "container started" which is too coarse for a real deploy.
