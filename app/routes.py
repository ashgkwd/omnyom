from flask import jsonify, request

from . import app
from .operations import create_feed, search


@app.route("/")
def hello_world():
    return {"message": "Hello, World!"}


@app.route("/feeds", methods=['POST'])
def feeds_create():
    feed_url = request.get_json()['url']
    feed = create_feed.execute(feed_url)
    return {"data": {"id": feed.id}}


@app.route("/feeds")
def feeds_index():
    feeds = list(search.execute())
    return jsonify({"data": feeds})


@app.route("/feeds/<feed_id>")
def feeds_show(feed_id: int):
    feed = search.find(feed_id)
    return jsonify({"data": feed})
