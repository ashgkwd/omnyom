from unittest.mock import Mock

import dramatiq
import pytest
from dramatiq import Worker
from sqlalchemy import select

from app import app as app_test
from app import db
from app.initializers.dramatiq_redis import broker
from app.models.feed import Feed
from app.models.feed_item import FeedItem


@pytest.fixture
def app():
    return app_test


@pytest.fixture
def stub_broker():
    broker.flush_all()
    return broker


@pytest.fixture
def stub_worker():
    worker = Worker(broker, worker_timeout=100)
    worker.start()
    yield worker
    worker.stop()


@pytest.fixture
def success_mock_and_actor():
    success_mock = Mock()

    @dramatiq.actor(max_retries=0)
    def success_actor(message_data, result_data):
        success_mock(message_data, result_data)
    return (success_mock, success_actor)


@pytest.fixture
def failure_mock_and_actor():
    failure_mock = Mock()

    @dramatiq.actor(max_retries=0)
    def failure_actor(message_data, exception_data):
        app_test.logger.error(
            f"failure actor received exception {exception_data}")
        failure_mock(message_data, exception_data)
    return (failure_mock, failure_actor)


@pytest.fixture
def post_headers():
    return {'Content-Type': 'application/json'}


@pytest.fixture
def feed_url():
    return "https://feeds.feedburner.com/tweakers/mixed"


@pytest.fixture
def feed_item_data():
    return {
        'title': 'Tribler 7.13.1',
        'title_detail': {'type': 'text/plain', 'language': None, 'base': 'https://feeds.feedburner.com/tweakers/mixed', 'value': 'Tribler 7.13.1'},
        'links': [{'rel': 'alternate', 'type': 'text/html', 'href': 'https://tweakers.net/downloads/67102/tribler-7131.html'}],
        'link': 'https://tweakers.net/downloads/67102/tribler-7131.html',
        'summary': 'Versie 7.13.1 van Tribler is uitgekomen. Tribler is een opensource-p2p-client, die ooit ontwikkeld is door studenten van de TU Delft en de VU Amsterdam. Tegenwoordig werkt een internationaal team wetenschappers uit meer dan twintig organisaties samen aan dit project. Tribler heeft onder meer een ingebouwde mediaspeler en er kan vaak direct worden gekeken of geluisterd wanneer een download wordt gestart. Verder kunnen er tokens worden verdiend door te seeden, die weer kunnen worden omgezet in andere valuta. Het programma is beschikbaar voor Windows, Linux en macOS. In deze uitgave zijn de volgende veranderingen en verbeteringen aangebracht: Tribler 7.13.1',
        'summary_detail': {'type': 'text/html', 'language': None, 'base': 'https://feeds.feedburner.com/tweakers/mixed', 'value': 'Versie 7.13.1 van Tribler is uitgekomen. Tribler is een opensource-p2p-client, die ooit ontwikkeld is door studenten van de TU Delft en de VU Amsterdam. Tegenwoordig werkt een internationaal team wetenschappers uit meer dan twintig organisaties samen aan dit project. Tribler heeft onder meer een ingebouwde mediaspeler en er kan vaak direct worden gekeken of geluisterd wanneer een download wordt gestart. Verder kunnen er tokens worden verdiend door te seeden, die weer kunnen worden omgezet in andere valuta. Het programma is beschikbaar voor Windows, Linux en macOS. In deze uitgave zijn de volgende veranderingen en verbeteringen aangebracht: Tribler 7.13.1'},
        'authors': [{'name': 'Bart van Klaveren'}],
        'author': 'Bart van Klaveren',
        'author_detail': {'name': 'Bart van Klaveren'},
        'tags': [{'term': 'Software-update / Software', 'scheme': None, 'label': None}],
        'comments': 'https://tweakers.net/downloads/67102/tribler-7131.html#reacties',
        'id': 'https://tweakers.net/downloads/67102',
        'guidislink': False,
        'published': 'Sun, 24 Dec 2023 21:08:41 GMT'
    }


@pytest.fixture
def ensure_feed(feed_url):
    with app_test.app_context():
        first_feed = db.session.query(Feed).first()
        if first_feed is None:
            feed = Feed(url=feed_url)
            db.session.add(feed)
            db.session.commit()
            return feed.id
        return first_feed.id


@pytest.fixture
def ensure_feed_without_items(feed_url, ensure_feed):
    feed_id = ensure_feed
    with app_test.app_context():
        feed_items = db.session.execute(select(FeedItem).where(
            FeedItem.feed_id == feed_id)).scalars()
        [db.session.delete(i) for i in feed_items]
        db.session.commit()
    return feed_id
