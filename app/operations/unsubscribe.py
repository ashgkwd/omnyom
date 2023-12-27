from app.models.feed import Feed

from .. import app, db
from . import search


def execute(feed_id):
    app.logger.debug(f"Removing a feed id: {feed_id}")
    feed = search.find(feed_id)
    db.session.delete(feed)
    db.session.commit()
    app.logger.debug(f"Removed feed with id {feed.id} and url {feed.url}")
    return feed
