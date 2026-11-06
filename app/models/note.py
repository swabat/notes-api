from app.models.base import Base
from datetime import datetime, timezone
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


def utc_now():
    return datetime.now(timezone.utc)


class Note(Base):
    __tablename__ = 'notes'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    content: Mapped[str | None] = mapped_column(String(10_000), nullable=True)
    is_archived: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"), nullable=True)
