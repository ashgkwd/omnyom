import json

from flask import url_for


def test_feeds_create(client, post_headers, feed_url):
    payload = json.dumps({'url': feed_url})
    response = client.post(url_for("feeds_create"),
                           headers=post_headers, data=payload)
    assert response.status_code == 200
    assert response.json.get('data').get('id') is not None


def test_feeds_index(client, feed_url):
    response = client.get(url_for("feeds_index"))
    assert response.status_code == 200
    assert response.json.get('data')[0].get('url') == feed_url
