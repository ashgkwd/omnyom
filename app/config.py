import os

dev_database_url = None
with open('/run/secrets/dev_database_secret') as f:
    dev_database_url = f.read().strip()

test_database_url = None
with open('/run/secrets/test_database_secret') as f:
    test_database_url = f.read().strip()


class Config:
    DEBUG = False
    DEVELOPMENT = False
    TEST = False
    REDIS_HOST = os.getenv("REDIS_HOST", "redis")
    SQLALCHEMY_DATABASE_URI = dev_database_url


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True


class TestConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    TEST = True
    SQLALCHEMY_DATABASE_URI = test_database_url
