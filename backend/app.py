from datetime import date, datetime, timedelta
from logging import error
from os import stat

from flask_jwt_extended import JWTManager, create_access_token, get_raw_jwt, current_user, jwt_required, jwt_optional
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from redis import Redis
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://flask:2b^XT8#iTO9d@database:5432/lineage'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

with open('secret_key.txt') as keyfile:
    app.config['SECRET_KEY'] = keyfile.read()

with open('jwt_secret_key.txt') as keyfile:
    app.config['JWT_SECRET_KEY'] = keyfile.read()

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']

TOKEN_STORE_EXPIRES_AFTER = timedelta(minutes=15)

token_store = Redis(host='revoked_token_store', port=6379, db=0, decode_responses=True)

api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

jwt.user_identity_loader(lambda user: user.username)
jwt.user_loader_callback_loader(lambda identity: User.query.filter_by(username=identity).first())
jwt.token_in_blacklist_loader(lambda decoded: token_store.exists(decoded['jti']))

def revoke_token(token):
    token_expires_at = datetime.fromtimestamp(token['exp'])
    time_to_expire = datetime.utcnow() - token_expires_at
    token_store.set(token['jti'], 1, time_to_expire)

class TimelineNode(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    timeline_id = db.Column(db.Integer, db.ForeignKey('timeline.uid'))
    position = db.Column(db.Integer)
    title = db.Column(db.String(32))
    content = db.Column(db.Text)
    attachment = db.Column(db.String(32))

    def __init__(self, timeline, title, content, attachment):
        self.timeline = timeline
        self.title = title
        self.content = content
        self.attachment = attachment
        self.position = len(timeline.nodes)

class TimelineNodeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TimelineNode
        include_fk = True

timeline_nodes_schema = TimelineNodeSchema(many=True)
timeline_node_schema = TimelineNodeSchema(many=False)

class Timeline(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.uid'))
    nodes = db.relationship('TimelineNode', backref='timeline', lazy='joined', order_by='TimelineNode.position')

    def next_node(self):
        return len(self.nodes)


class TimelineSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Timeline
        include_fk = True

    nodes = ma.Nested(TimelineNodeSchema, many=True)

timelines_schema = TimelineSchema(many=True)
timeline_schema = TimelineSchema(many=False)

class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password_hash = db.Column(db.String(144))
    timelines = db.relationship('Timeline', backref='owner', lazy='joined')

    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password, method='sha512')

    @classmethod
    def authenticate(cls, username, password):
        if any(i is None for i in (username, password)):
            return dict(error='missing fields'), 400

        user = cls.query.filter_by(username=username).first()
        if user is None or not check_password_hash(user.password_hash, password):
            return dict(error='incorrect credentials or user doesn\'t exist'), 401
        else:
            token = create_access_token(identity=user)
            return dict(username=user.username, token=token), 200
    
@app.route('/api/sanity')
def index():
    return jsonify('You\'re sane my guy!')

class Login(Resource):
    method_decorators = {
        'put': [jwt_required],
        'delete': [jwt_required]
    }

    @staticmethod
    def post():
        request_json = request.get_json()
        requested_username = request_json.get('username')
        requested_password = request_json.get('password')
        return User.authenticate(username=requested_username, password=requested_password)

    @staticmethod
    def put():
        token = get_raw_jwt()
        revoke_token(token)
        new_token = create_access_token(identity=current_user)
        return dict(token=new_token), 200

    @staticmethod
    def delete():
        token = get_raw_jwt()
        revoke_token(token)
        return None, 204

api.add_resource(Login, '/api/login')

class TimelineResource(Resource):
    method_decorators = [jwt_required]

    @staticmethod
    def get(timeline_id=None):
        user = current_user
        if timeline_id is not None:
            timeline = Timeline.query.filter_by(uid=timeline_id).first()
            if timeline is None:
                return dict(error='Invalid ID'), 404
            else:
                return dict(timeline_schema.dump(timeline))
        else:
            timelines = Timeline.query.filter_by(owner=user).all()
            return timelines_schema.dump(timelines)

    @staticmethod
    def post(timeline_id):
        if timeline_id is None:
            user = current_user
            params = request.json
            name = params.get('name')
            timeline = Timeline(title=name, owner=user)
            db.session.add(timeline)
            db.session.commit()
            return timeline_schema.dump(timeline)

api.add_resource(TimelineResource, '/api/timelines', '/api/timeline/<int:timeline_id>')

class TimelineNodeResource(Resource):
    method_decorators = [jwt_required]

    @staticmethod
    def get(timeline_id=None, node_id=None):
        if timeline_id is None:
            return dict(error='Missing timeline ID'), 404
        elif node_id is None:
            timeline = Timeline.query.filter_by(uid=timeline_id).first()
            if timeline is None:
                return dict(error='Timeline ID invalid'), 404
            return timeline_nodes_schema.dump(timeline.nodes)
        else:
            timeline = Timeline.query.filter_by(uid=timeline_id).first()
            if timeline is None:
                return dict(error='Timeline ID invalid'), 404

            node = TimelineNode.query.filter_by(timeline=timeline, position=node_id).first()
            if node is None:
                return dict(error='Node ID invalid'), 404
            return timeline_node_schema.dump(node)

    @staticmethod
    def post(timeline_id=None):
        if timeline_id is None:
            return dict(error='Missing timeline ID'), 404

        timeline = Timeline.query.filter_by(uid=timeline_id).first()
        if timeline is None:
            return dict(error='Invalid ID'), 404

        params = request.json
        title = params.get('title')
        content = params.get('content')
        attachment = params.get('attachment')
        if any(param is None for param in (title, content)):
            return dict(error='Missing required fields'), 400

        new_node = TimelineNode(timeline=timeline, title=title, content=content, attachment=attachment)
        db.session.add(new_node)
        db.session.commit()
        return timeline_node_schema.dump(new_node), 201
    
    @staticmethod
    def patch(timeline_id=None, node_id=None):
        if timeline_id is None:
            return dict(error='Missing timeline ID'), 404

        timeline = Timeline.query.filter_by(uid=timeline_id).first()
        if timeline is None:
            return dict(error='Invalid ID'), 404

        params = request.json
        allowed_fields = ('title', 'content', 'attachment')
        filtered = {key: params[key] for key in allowed_fields if key in params}
        node = TimelineNode.query.filter_by(timeline=timeline, position=node_id)
        if node is None:
            return dict(error='Node ID invalid'), 404
        for property, new_value in filtered.items():
            setattr(node, property, new_value)
        return timeline_node_schema.dump(node)

api.add_resource(TimelineNodeResource, '/api/timeline/<int:timeline_id>/nodes', '/api/timeline/<int:timeline_id>/node/<int:node_id>')
    

@app.route('/api/register', methods=['POST'])
def register():
    request_json = request.get_json()
    requested_username = request_json.get('username')
    requested_password = request_json.get('password')
    new_user = User(username=requested_username, password=requested_password)
    try:
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        return jsonify({'error': 'username is taken'}), 409
    else:
        return User.authenticate(username=requested_username, password=requested_password)[0], 201