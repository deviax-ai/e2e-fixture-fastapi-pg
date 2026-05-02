"""Pydantic schemas."""
from datetime import datetime

from pydantic import BaseModel


class NoteIn(BaseModel):
    body: str


class NoteOut(BaseModel):
    id: int
    body: str
    created_at: datetime

    class Config:
        from_attributes = True
