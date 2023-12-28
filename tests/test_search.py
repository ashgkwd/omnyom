import json
import time

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


def test_search_for_one_feed(client, ensure_feed, second_feed_url, post_headers):
    feed_id = ensure_feed
    response = client.get(url_for("search_feed_items", feed_id=feed_id))
    assert response.status_code == 200
    data = response.json.get('data')
    assert len(data) > 0
    assert {feed_item['feed_id'] for feed_item in data} == {feed_id}

    payload = json.dumps({'url': second_feed_url, 'perform_sync': True})
    response = client.post(
        url_for("create_subscription"),
        headers=post_headers, data=payload
    )
    assert response.status_code == 200
    second_feed_id = response.json.get('data').get('id')
    assert second_feed_id is not None

    response = client.get(url_for("search_feed_items", feed_id=second_feed_id))
    assert response.status_code == 200
    data = response.json.get('data')
    assert len(data) > 0
    assert {feed_item['feed_id'] for feed_item in data} == {second_feed_id}


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
