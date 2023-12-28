import app.initializers.dramatiq_redis
from app import app
from app.operations import refresh, search


def refresh_feeds():
    with app.app_context():
        app.logger.debug("Starting a refresh feeds command from cron")
        feeds = search.feeds()
        for feed in feeds:
            refresh.execute_async.send(feed.id, feed.url)


if __name__ == "__main__":
    refresh_feeds()
