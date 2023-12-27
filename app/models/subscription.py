from dataclasses import dataclass
from typing import List

from sqlalchemy import DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app import db


@dataclass
class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    id: Mapped[int] = mapped_column(primary_key=True)
    feed_id: Mapped[int] = mapped_column(ForeignKey("feeds.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=func.now())
    UniqueConstraint(feed_id, user_id, name="user_feed_subscription_index")
    feed: Mapped["Feed"] = relationship()
    user: Mapped["User"] = relationship()
