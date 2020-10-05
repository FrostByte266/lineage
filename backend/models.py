from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash

from .shared import db, redis, jwt

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

class Timeline(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.uid'))
    nodes = db.relationship('TimelineNode', backref='timeline', lazy='joined', order_by='TimelineNode.position')

    @property
    def next_node(self):
        return len(self.nodes)

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
        """Authenticates details of a user

        Parameters
        ----------
        username : str
            The username of the user to authenticate
        password : str
            The password to authenticate with

        Returns
        -------
        User
            The authenticated user
        """
        if any(i is None for i in (username, password)):
            return dict(error='missing fields'), 400

        user = cls.query.filter_by(username=username).first()
        if user is None or not check_password_hash(user.password_hash, password):
            return dict(error='incorrect credentials or user doesn\'t exist'), 401
        else:
            token = create_access_token(identity=user)
            return dict(username=user.username, token=token), 200