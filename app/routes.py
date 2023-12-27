from flask import jsonify, request

# NOTE: Importing initializer here to ensure correct broker is picked
import app.initializers.dramatiq_redis

from . import app
from .operations import refresh, search, subscribe, unsubscribe


@app.route("/")
def hello_world():
    return {"message": "Hello, World!"}


@app.route("/subscribe", methods=['POST'])
def create_subscription():
    feed_url = request.get_json()['url']
    feed = subscribe.execute(feed_url)
    return {"data": {"id": feed.id}}


@app.route("/unsubscribe/<feed_id>", methods=['DELETE'])
def remove_subscription(feed_id: int):
    feed = unsubscribe.execute(feed_id)
    return {"data": feed}


@app.route("/feeds")
def feeds_index():
    feeds = list(search.execute())
    return jsonify({"data": feeds})


@app.route("/feeds/<feed_id>")
def feeds_show(feed_id: int):
    feed = search.find(feed_id)
    if feed is not None:
        return jsonify({"data": feed})
    return {"error": "feed not found"}
