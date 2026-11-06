from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    content: str | None = Field(default=None, max_length=10_000)
    category_id: int | None = None


class NoteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str | None
    is_archived: bool
    created_at: datetime
    updated_at: datetime
    category_id: int | None

class NoteUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=150)
    content: str | None = Field(default=None, max_length=10_000)
    category_id: int | None = None