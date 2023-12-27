from dataclasses import dataclass
from typing import List

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app import db


@dataclass
class Feed(db.Model):
    __tablename__ = 'feeds'
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    created_by_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=func.now())
    created_by: Mapped["User"] = relationship()
    feed_items: Mapped[List["FeedItem"]] = relationship()
