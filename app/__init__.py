# Flask app setup
import os

from flask import Flask

app = Flask(__name__)
env_config = os.getenv("APP_SETTINGS", "app.config.DevelopmentConfig")
app.config.from_object(env_config)

# SQLAlchemy setup
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

# Flask-Migrate setup
from flask_migrate import Migrate

migrate = Migrate(app, db)

# Initializers, models and routes
from . import routes
