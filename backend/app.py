from datetime import timedelta

import yaml
from flask import Flask
from flask_migrate import Migrate

from .models import User
from .api import api_blueprint
from .shared import db, redis, jwt
from .schemas import ma

with open('base_config.yaml') as f:
    basic_conf = yaml.load(f, yaml.BaseLoader)

with open('secret_config.yaml') as f:
    secret_conf = yaml.load(f, yaml.BaseLoader)

app = Flask(__name__)
app.config.update(basic_conf)
app.config.update(secret_conf)
TOKEN_STORE_EXPIRES_AFTER = timedelta(minutes=15)

jwt.user_identity_loader(lambda user: user.username)
jwt.user_loader_callback_loader(lambda identity: User.query.filter_by(username=identity).first())
jwt.token_in_blacklist_loader(lambda decoded: redis.exists(decoded['jti']))

db.init_app(app)
redis.init_app(app)
jwt.init_app(app)
ma.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(api_blueprint, url_prefix='/api')
