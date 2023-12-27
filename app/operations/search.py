from sqlalchemy import select

from app import db
from app.models.feed import Feed


def execute(filter_by=None):
    smt = select(Feed)
    if filter_by is not None:
        is_read = True if filter_by == 'read' else False
        smt = smt.where(FeedItemRead.is_read == is_read)
    smt = smt.order_by(Feed.created_at)
    return db.session.execute(smt).scalars()


def find(feed_id):
    return db.session.query(Feed).filter(Feed.id == feed_id).first()
