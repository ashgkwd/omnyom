from app.models.feed_item import FeedItem


def test_feed_item_from_dict(feed_item_data):
    feed_id = 12
    creator = FeedItem.from_dict(with_feed_id=feed_id)
    feed_item = creator(feed_itemable=feed_item_data)
    assert feed_item.external_id is not None
    assert feed_item.external_id == feed_item_data['id']
    assert feed_item.title == feed_item_data['title']
    assert feed_item.author == feed_item_data['author']
    assert feed_item.summary == feed_item_data['summary']
    assert feed_item.feed_id == feed_id


def test_feed_item_from_dict_on_list(feed_item_data):
    feed_id = 12
    items = [feed_item_data]
    feed_items = list(map(FeedItem.from_dict(with_feed_id=feed_id), items))
    assert len(feed_items) == 1
    assert feed_items[0].external_id == feed_item_data['id']
