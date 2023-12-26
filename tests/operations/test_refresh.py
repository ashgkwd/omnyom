from unittest.mock import patch

from app import app
from app.models.feed_item import FeedItem
from app.operations import refresh, search


def test_refresh():
    with app.app_context():
        feed = search.execute().first()
        app.logger.debug(feed)
        feed_items = list(refresh.execute(feed.id, feed.url))
        app.logger.debug("Test received feed items")
        app.logger.debug(len(feed_items))
        assert type(feed_items) is list
        assert type(feed_items[0]) is FeedItem
        assert feed_items[0].id is not None


def test_refresh_async(stub_broker, stub_worker, success_mock_and_actor, failure_mock_and_actor):
    with app.app_context():
        feed = search.execute().first()
        app.logger.debug(feed)
        success_mock, success_actor = success_mock_and_actor
        failure_mock, failure_actor = failure_mock_and_actor

        message = refresh.execute_async.send_with_options(
            args=(feed.id, feed.url),
            on_failure=failure_actor,
            on_success=success_actor
        )
        stub_broker.join(refresh.execute_async.queue_name)
        stub_worker.join()
        assert message.queue_name == 'default'
        assert message.actor_name == 'execute_async'
        assert message.args == (feed.id, feed.url)
        assert message.message_id is not None
        success_mock.assert_called_once()
        failure_mock.assert_not_called()


def test_refresh_async_with_failure(stub_broker, stub_worker, success_mock_and_actor, failure_mock_and_actor):
    with app.app_context():
        feed = search.execute().first()
        app.logger.debug(feed)
        success_mock, success_actor = success_mock_and_actor
        failure_mock, failure_actor = failure_mock_and_actor

        with patch('app.operations.refresh.feedparser.parse', side_effect=[KeyError("test error"), {'entries': []}]) as patched_feedparser:
            message = refresh.execute_async.send_with_options(
                args=(feed.id, feed.url),
                on_failure=failure_actor,
                on_success=success_actor
            )
            stub_broker.join(refresh.execute_async.queue_name)
            stub_worker.join()
            assert message.queue_name == 'default'
            assert message.actor_name == 'execute_async'
            assert message.args == (feed.id, feed.url)
            assert message.message_id is not None
            failure_mock.assert_called_once()
            success_mock.assert_called_once()
            assert patched_feedparser.call_count == 2


def xtest_refresh_async_with_dead_letter(stub_broker, stub_worker, success_mock_and_actor, failure_mock_and_actor):
    pass
