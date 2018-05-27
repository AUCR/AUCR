"""The auth models.py defines all the database tables we need for our auth plugin."""
# coding=utf-8
import udatetime
import base64
import ujson as json
import os
import jwt
import redis
import rq
import onetimepass
from app import login
from app import db
from datetime import timedelta
from hashlib import md5
from time import time
from flask import current_app, url_for
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash
from flask_bcrypt import check_password_hash
from yaml_info.yamlinfo import YamlInfo
from app.plugins.reports.storage.elastic_search import add_to_index, remove_from_index, query_index


class SearchableMixin(object):
    """Process ES interaction with the sql tables."""

    @classmethod
    def search(cls, expression, page, per_page):
        """Return searchable data from ES."""
        ids, total = query_index(str(cls.__tablename__), expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        """Check ES before index commit."""
        session._changes = {
            'add': [obj for obj in session.new if isinstance(obj, cls)],
            'update': [obj for obj in session.dirty if isinstance(obj, cls)],
            'delete': [obj for obj in session.deleted if isinstance(obj, cls)]
        }

    @classmethod
    def after_commit(cls, session):
        """Return changed database searchable tagged fields in ES."""
        if session._changes:
            for obj in session._changes['add']:
                add_to_index(cls.__tablename__, obj)
            for obj in session._changes['update']:
                add_to_index(cls.__tablename__, obj)
            for obj in session._changes['delete']:
                remove_from_index(cls.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        """Process changed messages by after_commit and reindex values in ES."""
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


class PaginatedAPIMixin(object):
    """API Uses and Paginated calls."""

    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        """Take a query and return json object."""
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page, **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page, **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page, **kwargs) if resources.has_prev else None
            }
        }
        return data


class User(UserMixin, PaginatedAPIMixin, db.Model):
    """AUCR User models class defines information in the user table."""

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=udatetime.utcnow)
    token = db.Column(db.String(120), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    groups = db.relationship('Group', foreign_keys='Group.username_id', backref='author', lazy='dynamic')
    messages_sent = db.relationship('Message', foreign_keys='Message.sender_id', backref='author', lazy='dynamic')
    messages_received = db.relationship('Message', foreign_keys='Message.recipient_id',
                                        backref='recipient', lazy='dynamic')
    last_message_read_time = db.Column(db.DateTime)
    notifications = db.relationship('Notification', backref='user', lazy='dynamic')
    tasks = db.relationship('Task', backref='user', lazy='dynamic')
    otp_secret = db.Column(db.String(120))

    def __repr__(self):
        """Return string representation of the User Database Object Table."""
        return '<User {}>'.format(self.username)

    def __init__(self, **kwargs):
        """Create the User init of the User Database table object."""
        super(User, self).__init__(**kwargs)

    def set_otp_secret(self):
        """Set two factor token for user."""
        if self.otp_secret is None:
            # generate a random secret
            self.otp_secret = base64.b32encode(os.urandom(64)).decode('utf-8')

    def set_password(self, password):
        """Set the user password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify bcrypt stored hash against password parameter."""
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        """Return user avatar from gravatar.com."""
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def get_reset_password_token(self, expires_in=600):
        """Return user reset password token."""
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in}, current_app.config['SECRET_KEY'],
                          algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        """Check reset password token and return outcome."""
        try:
            user_id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except AttributeError:
            return
        return User.query.get(user_id)

    def new_messages(self):
        """Check and return new messages for current user."""
        last_read_time = self.last_message_read_time or udatetime.from_string("1900-01-01T00:00:00.000000")
        return Message.query.filter_by(recipient=self).filter(Message.timestamp > last_read_time).count()

    def add_notification(self, name, data):
        """Create notification message for a user."""
        self.notifications.filter_by(name=name).delete()
        n = Notification(name=name, payload_json=json.dumps(data), user=self)
        db.session.add(n)
        return n

    def launch_task(self, name, description, *args, **kwargs):
        """Create task in AUCR redis mq."""
        rq_job = current_app.task_queue.enqueue('app.tasks.' + name, self.id, *args, **kwargs)
        task = Task(id=rq_job.get_id(), name=name, description=description, user=self)
        db.session.add(task)
        return task

    def get_tasks_in_progress(self):
        """Return tasks progress from AUCR redis mq service."""
        return Task.query.filter_by(user=self, complete=False).all()

    def get_task_in_progress(self, name):
        """Return a single task progress from the AUCR redis mq service."""
        return Task.query.filter_by(name=name, user=self, complete=False).first()

    def to_dict(self, include_email=False):
        """Return dictionary object type for API calls."""
        data = {
            'id': self.id,
            'username': self.username,
            'last_seen': self.last_seen.isoformat() + 'Z',
            'about_me': self.about_me,
            '_links': {
                'self': url_for('api.get_user', id=self.id),
                'avatar': self.avatar(128)
            }
        }
        if include_email:
            data['email'] = self.email
        return data

    def from_dict(self, data, new_user=False):
        """Process from dictionary object type for API Posts."""
        for field in ['username', 'email', 'about_me']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def get_token(self, expires_in=3600):
        """Generate and return a token for user auth."""
        now = udatetime.utcnow().replace(tzinfo=None)
        if self.token and self.token_expiration > now - timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(64)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        """Check and expire user token if expiration time is True."""
        self.token_expiration = \
            udatetime.utcnow().replace(tzinfo=None) - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        """Check a token against user token."""
        now = udatetime.utcnow().replace(tzinfo=None)
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < now:
            return None
        return user

    def get_totp_uri(self):
        """Return two factor token uri path."""
        return 'otpauth://totp/AUCR:{0}?secret={1}&issuer=AUCR' \
            .format(self.username, self.otp_secret)

    def verify_totp(self, token):
        """Check and return if user two factor token for AUCR auth plugin matches."""
        return onetimepass.valid_totp(token, self.otp_secret)


class Group(db.Model):
    """AUCR Group Table Database Module."""

    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    groups_id = db.Column(db.Integer, db.ForeignKey('groups.id'), index=True)
    username_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, index=True, default=udatetime.utcnow)

    def __repr__(self):
        """Return string representation of Group Database Object Table."""
        return '<Group {}>'.format(self.group_id)

    def to_dict(self):
        """Return dictionary object type for Group database Table API calls."""
        group_object = Groups.query.filter_by(id=self.id).first()
        data = {
            'id': self.id,
            'groups_id': group_object.groups.id,
            'username_id': self.username_id,
            'time_stamp': self.timestamp.isoformat() + 'Z',
        }
        return data


class Groups(db.Model):
    """Group Database Table Module."""

    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    timestamp = db.Column(db.DateTime, index=True, default=udatetime.utcnow)

    def __repr__(self):
        """Return string representation of the Groups Database Object Table."""
        return '<Groups {}>'.format(self.name)

    def to_dict(self):
        """Return dictionary object type for Group table database API calls."""
        data = {
            'id': self.id,
            'name': self.name,
            'last_seen': self.timestamp.isoformat() + 'Z'}
        return data


def insert_initial_user_values(*args, **kwargs):
    """Create default database values from auth yaml template file."""
    run = YamlInfo("app/plugins/auth/auth.yml", "none", "none")
    admin_data = run.get()
    for items in admin_data:
        hashed_password = generate_password_hash(admin_data[items]["password"])
        default_groups = Groups.__call__(name="admin")
        default_user_groups = Groups.__call__(name="user")
        db.session.add(default_groups)
        db.session.add(default_user_groups)
        db.session.commit()
        default_admin = User.__call__(username=items, password_hash=hashed_password, email=admin_data[items]["email"])
        admin_group = Group.__call__(groups_id=1, username_id=1)
        user_group = Group.__call__(groups_id=2, username_id=1)
        db.session.add(admin_group)
        db.session.add(user_group)
        db.session.add(default_admin)
        db.session.commit()


db.event.listen(Group.__table__, 'after_create', insert_initial_user_values)


@login.user_loader
def load_user(user_id):
    """User load callback for Flask-Login."""
    return User.query.get(int(user_id))


class Post(SearchableMixin, db.Model):
    __searchable__ = ['body']
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=udatetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    language = db.Column(db.String(5))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


db.event.listen(db.session, 'before_commit', Post.before_commit)
db.event.listen(db.session, 'after_commit', Post.after_commit)


class Message(SearchableMixin, db.Model):
    """Database table for User messages."""

    __searchable__ = ['body']
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=udatetime.utcnow)

    def __repr__(self):
        """Return string representation of the Message Database Object Table."""
        return '<Message {}>'.format(self.body)


db.event.listen(db.session, 'before_commit', Message.after_commit)
db.event.listen(db.session, 'after_commit', Message.after_commit)


class Notification(db.Model):
    """AUCR auth plugin Database table for User Notification."""

    __tablename__ = 'notification'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.Float, index=True, default=time)
    payload_json = db.Column(db.Text)

    def get_data(self):
        """Return string representation of the Notification Database Object Table."""
        return json.loads(str(self.payload_json))


class Task(db.Model):
    """AUCR's database table for redis mq service."""

    __tablename__ = 'task_mq'
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(128), index=True)
    description = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    complete = db.Column(db.Boolean, default=False)

    def get_rq_job(self):
        """Return redis mq job."""
        try:
            rq_job = rq.job.Job.fetch(self.id, connection=current_app.redis)
        except (redis.exceptions.RedisError, rq.exceptions.NoSuchJobError):
            return None
        return rq_job

    def get_progress(self):
        """Return message progress from redis mq."""
        job = self.get_rq_job()
        return job.meta.get('progress', 0) if job is not None else 100


class Award(db.Model):
    """AUCR point system award table."""

    __tablename__ = 'award'
    id = db.Column(db.Integer, primary_key=True)
    award_name = db.Column(db.String(128), index=True)
    username = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, index=True, default=udatetime.utcnow)

    def __repr__(self):
        """Return string representation of the Award Object."""
        return '<Award {}>'.format(self.award_name)
