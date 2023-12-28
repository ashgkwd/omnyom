import json

from flask import url_for


def test_mark_feed_item_as_read(client, post_headers, feed_item):
    payload = json.dumps({'mark': 'read'})
    feed_item_id = feed_item
    response = client.post(
        url_for("feed_items_mark", feed_item_id=feed_item_id),
        headers=post_headers,
        data=payload
    )
    assert response.status_code == 200
    assert response.json.get('data').get('message') == "marked item as read"


def test_mark_feed_item_as_unread(client, post_headers, feed_item):
    payload = json.dumps({'mark': 'unread'})
    feed_item_id = feed_item
    response = client.post(
        url_for("feed_items_mark", feed_item_id=feed_item_id),
        headers=post_headers,
        data=payload
    )
    assert response.status_code == 200
    assert response.json.get('data').get('message') == "marked item as unread"
