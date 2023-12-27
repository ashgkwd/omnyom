from dataclasses import dataclass
from typing import Optional

from sqlalchemy import JSON, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app import db


@dataclass
class FeedItem(db.Model):
    __tablename__ = 'feed_items'
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    external_id: Mapped[str] = mapped_column(
        String, unique=True, nullable=False)
    title: Mapped[str]
    author: Mapped[str]
    summary: Mapped[str]
    published_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=True))
    extras: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    content: Mapped[Optional[str]]
    feed_id: Mapped[int] = mapped_column(
        ForeignKey("feeds.id"), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=func.now())
    feed_item_read: Mapped["FeedItemRead"] = relationship(
        cascade="all, delete-orphan")

    @classmethod
    def from_dict(cls, with_feed_id: int):
        def feed_item_with_feed_id(feed_itemable):
            init_cols = ['title', 'author', 'summary']
            init_params = {x: feed_itemable[x] for x in init_cols}
            init_params["feed_id"] = with_feed_id
            init_params["external_id"] = feed_itemable["id"]
            init_params["url"] = feed_itemable["link"]
            init_params["published_at"] = feed_itemable["published"]
            return cls(**init_params)
        return feed_item_with_feed_id
