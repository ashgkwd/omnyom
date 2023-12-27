from app.models.feed import Feed

from .. import app, db


def execute(feed_url):
    app.logger.debug(f"Creating a feed for url: {feed_url}")
    feed = Feed(url=feed_url)
    db.session.add(feed)
    db.session.commit()
    app.logger.debug(f"Created feed with id {feed.id} and url {feed.url}")
    return feed
