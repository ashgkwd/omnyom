import json

from flask import url_for


def test_search_without_filters(client, ensure_feed):
    response = client.get(url_for("search_feed_items"))
    assert response.status_code == 200
    assert len(response.json.get('data')) > 0


def test_search_read(client, ensure_feed):
    response = client.get(url_for("search_feed_items", marked_as='read'))
    assert response.status_code == 200
    assert len(response.json.get('data')) == 0


def test_search_unread(client, ensure_feed):
    response = client.get(url_for("search_feed_items", marked_as='unread'))
    assert response.status_code == 200
    assert len(response.json.get('data')) > 0


def test_search_with_some_reads(client, post_headers, feed_item):
    """
    This test will
    1. get total feed items count
    2. mark one feed item as read
    3. filter by read and assert count to 1
    4. filter by unread and assert count to total - 1
    """
    response = client.get(url_for("search_feed_items"))
    assert response.status_code == 200
    total_feed_items = len(response.json.get('data'))
    assert total_feed_items > 0

    payload = json.dumps({'mark': 'read'})
    feed_item_id = feed_item
    response = client.post(
        url_for("feed_items_mark", feed_item_id=feed_item_id),
        headers=post_headers,
        data=payload
    )
    assert response.status_code == 200

    response = client.get(url_for("search_feed_items", marked_as='read'))
    assert response.status_code == 200
    assert len(response.json.get('data')) == 1

    response = client.get(url_for("search_feed_items", marked_as='unread'))
    assert response.status_code == 200
    assert len(response.json.get('data')) == total_feed_items - 1
