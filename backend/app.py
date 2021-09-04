import os
from datetime import timedelta

import yaml
from flask import Flask
from flask_migrate import Migrate

from api import api_blueprint
from models import User
from schemas import ma
from shared import db, jwt, redis

os.chdir('/app')

# Load generic config options
with open('base_config.yaml') as f:
    basic_conf = yaml.safe_load(f)

# Load secret keys
with open('secret_config.yaml') as f:
    secret_conf = yaml.safe_load(f)

# Create Flask app and set config values
app = Flask(__name__)
app.config.update(basic_conf)
app.config.update(secret_conf)
TOKEN_STORE_EXPIRES_AFTER = timedelta(minutes=15)

# Register callbacks for JWT manager
jwt.user_identity_loader(lambda user: user.username)
jwt.user_loader_callback_loader(lambda identity: User.query.filter_by(username=identity).first())
jwt.token_in_blacklist_loader(lambda decoded: redis.exists(decoded['jti']))

# Connect app with plugins
db.init_app(app)
redis.init_app(app)
jwt.init_app(app)
ma.init_app(app)
migrate = Migrate(app, db)

# Mount the API blueprint to the app
app.register_blueprint(api_blueprint, url_prefix='/api')
