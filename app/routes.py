from flask import jsonify, request

from . import app

# from .operations import create_feed, search


@app.route("/")
def hello_world():
    return {"message": "Hello, World!"}
