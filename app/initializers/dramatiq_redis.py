import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.brokers.stub import StubBroker

from app import app

if app.config.get('TEST'):
    broker = StubBroker()
    broker.emit_after("process_boot")
else:
    broker = RedisBroker(host=app.config.get('REDIS_HOST'))

dramatiq.set_broker(broker)
