from sqlalchemy import select

from app import db
from app.models.feed import Feed


def execute():
    smt = select(Feed).order_by(Feed.created_at)
    return db.session.execute(smt).scalars()


def find(feed_id):
    return db.session.query(Feed).filter(Feed.id == feed_id).first()
