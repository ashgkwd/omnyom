from dataclasses import dataclass
from typing import List

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app import db


@dataclass
class FeedItemRead(db.Model):
    __tablename__ = 'feed_item_reads'
    id: Mapped[int] = mapped_column(primary_key=True)
    feed_item_id: Mapped[int] = mapped_column(
        ForeignKey("feed_items.id"),
        unique=True,
        nullable=False
    )
    is_read: Mapped[bool] = mapped_column(nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=func.now()
    )
