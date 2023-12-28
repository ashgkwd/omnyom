from app.models.feed import Feed

from .. import app, db
from . import refresh


def execute(feed_url, perform_sync=False):
    app.logger.debug(
        f"Creating a feed for url: {feed_url}, is performing sync {perform_sync}")
    feed = Feed(url=feed_url)
    db.session.add(feed)
    db.session.commit()
    if perform_sync:
        refresh.execute(feed.id, feed_url)
    else:
        refresh.execute_async.send(feed.id, feed_url)
    app.logger.debug(f"Created feed with id {feed.id} and url {feed.url}")
    return feed
