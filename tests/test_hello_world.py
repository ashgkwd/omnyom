import json
import os

from app import app


def test_uses_correct_config():
    assert os.getenv("APP_SETTINGS") == "app.config.TestConfig"


def test_index_route(client):
    response = client.get('/')

    assert response.status_code == 200
    assert json.loads(response.data.decode('utf-8')
                      )['message'] == 'Hello, World!'
