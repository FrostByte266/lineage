from datetime import datetime

from flask import Blueprint, request, jsonify, Response
from flask_jwt_extended import create_access_token, get_raw_jwt, current_user, jwt_required, jwt_optional
from flask_restful import Api, Resource
from sqlalchemy.exc import IntegrityError

from .models import User, Timeline, TimelineNode
from .schemas import timeline_node_schema, timeline_nodes_schema, timeline_schema, timelines_schema
from .shared import db, redis

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)

def revoke_token(token):
    token_expires_at = datetime.fromtimestamp(token['exp'])
    time_to_expire = token_expires_at - datetime.utcnow()
    redis.set(token['jti'], 1, time_to_expire)

class Login(Resource):
    method_decorators = {
        'put': [jwt_required],
        'delete': [jwt_required],
        'get': [jwt_optional]
    }

    @staticmethod
    def get():
        return Response(status=204 if current_user else 401)

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

api.add_resource(Login, '/login')

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
    def post(timeline_id=None):
        if timeline_id is None:
            user = current_user
            params = request.json
            name = params.get('name')
            timeline = Timeline(title=name, owner=user)
            db.session.add(timeline)
            db.session.commit()
            return timeline_schema.dump(timeline)

api.add_resource(TimelineResource, '/timelines', '/timeline/<int:timeline_id>')

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
        node = TimelineNode.query.filter_by(timeline=timeline, position=node_id).first()
        if node is None:
            return dict(error='Node ID invalid'), 404
        for property, new_value in filtered.items():
            setattr(node, property, new_value)
        db.session.commit()
        return timeline_node_schema.dump(node)

api.add_resource(TimelineNodeResource, '/timeline/<int:timeline_id>/nodes', '/timeline/<int:timeline_id>/node/<int:node_id>')

@api_blueprint.route('/register', methods=['POST'])
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