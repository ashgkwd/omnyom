from sqlalchemy import and_, exists, select

from app import app, db
from app.models.feed import Feed
from app.models.feed_item import FeedItem
from app.models.feed_item_read import FeedItemRead


def execute(marked_as=None, feed_id=None):
    app.logger.debug(
        f"Search with marked_as={marked_as} and feed_id={feed_id}")
    smt = select(FeedItem)
    if marked_as is not None:
        if marked_as == 'read':
            smt = smt.join(FeedItemRead, isouter=False).where(
                FeedItemRead.is_read == True)
        else:
            smt = smt.where(~exists().where(
                and_(FeedItemRead.is_read == True,
                     FeedItemRead.feed_item_id == FeedItem.id)
            ))
    if feed_id is not None:
        smt = smt.where(FeedItem.feed_id == feed_id)
    smt = smt.order_by(FeedItem.published_at)
    app.logger.debug(f"statement to be run through search: {smt}")
    return db.session.execute(smt).scalars()


def feeds():
    smt = select(Feed).order_by(Feed.created_at)
    return db.session.execute(smt).scalars()


def find(feed_id):
    return db.session.query(Feed).filter(Feed.id == feed_id).first()
