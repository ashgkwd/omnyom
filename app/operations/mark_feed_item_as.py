from app.models.feed_item_read import FeedItemRead

from .. import db


def execute(feed_item_id, mark_as='read'):
    """
    Marks the given feed item for 'the user' as read or not read

    Args:
    - feed_item_id: int -- id of the feed item to be marked
    - mark_as: str -- one of 'read' or 'unread'. Defaults to 'read'
    """
    mark = mark_as == 'read'
    feed_item_read = db.session.query(FeedItemRead).filter(
        FeedItemRead.feed_item_id == feed_item_id).first()
    if feed_item_read is None:
        feed_item_read = FeedItemRead(feed_item_id=feed_item_id, is_read=mark)
    else:
        feed_item_read.is_read = mark

    db.session.add(feed_item_read)
    db.session.commit()
    return feed_item_read
