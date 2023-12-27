import dramatiq
import feedparser

from app import app, db
from app.models.feed_item import FeedItem


def existing_feed_item_ids(external_ids):
    result = db.session.query(FeedItem.external_id).filter(
        FeedItem.external_id.in_(list(external_ids)))
    return {item.external_id for item in result}


def filter_new_feed_items(items):
    external_ids = set(map(lambda i: i['id'], items))
    existing_ids = existing_feed_item_ids(external_ids)
    new_feed_item_ids = external_ids - existing_ids
    # app.logger.debug(f"External feed item ids {external_ids}")
    # app.logger.debug(f"Existing feed item ids {existing_ids}")
    # app.logger.debug("New feed item ids 🏮")
    # app.logger.debug(new_feed_item_ids)
    return list(filter(lambda i: i.id in new_feed_item_ids, items))


def create_feed_items(items: list, feed_id: int):
    app.logger.debug(f"Creation will be performed on {len(items)}")
    feed_items = list(map(FeedItem.from_dict(with_feed_id=feed_id), items))
    app.logger.debug("Feed items ready to be saved are")
    # app.logger.debug(feed_items[0]) if len(feed_items) > 0 else None
    db.session.add_all(feed_items)
    db.session.commit()
    return feed_items


def execute(feed_id, feed_url):
    app.logger.debug(f"Refreshing feed id {feed_id} and url {feed_url}")
    response = feedparser.parse(feed_url)
    app.logger.debug("Received response data")
    # app.logger.debug(response['entries'][0]) if len(
    #     response['entries']) > 0 else None
    return create_feed_items(filter_new_feed_items(response['entries']), feed_id)


@dramatiq.actor(max_retries=3)
def execute_async(feed_id, feed_url):
    with app.app_context():
        return execute(feed_id, feed_url)
