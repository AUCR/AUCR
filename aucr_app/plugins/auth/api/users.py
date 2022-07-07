"""AUCR main auth plugin apiv2 features."""
# coding=utf-8
from flask import jsonify, request, Blueprint
from aucr_app import db
from aucr_app.plugins.auth.models import User
from aucr_app.plugins.errors.api.errors import bad_request
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

api_page = Blueprint('usersapiv2', __name__, template_folder='templates')
token_auth = HTTPTokenAuth()


@api_page.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    """Return User id from database."""
    return jsonify(User.query.get_or_404(id).to_dict())


@api_page.route('/users', methods=['GET'])
@token_auth.login_required
def get_users():
    """Return user list."""
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(User.query, page, per_page, 'apiv2.get_users')
    return jsonify(data)


@api_page.route('/users', methods=['POST'])
def create_user():
    """API Create new user."""
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include username, email and password fields')
    new_user = data['username']
    current_user = User.query.filter_by(username=new_user).first()
    new_email = data['email']
    current_email = User.query.filter_by(email=new_email).first()
    if current_user:
        return bad_request('please use a different username')
    if current_email:
        return bad_request('please use a different email address')
    user = User(username=new_user, email=new_email)
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()

    user.from_dict(data, new_user=True)
    response = jsonify(user.to_dict())
    response.status_code = 201
    return response


@api_page.route('/users/<int:id_>', methods=['PUT'])
@token_auth.login_required
def update_user(id_):
    """API Update user account."""
    user = User.query.get_or_404(id_)
    data = request.get_json() or {}
    if 'username' in data and data['username'] != user.username and \
            User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if 'email' in data and data['email'] != user.email and User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())
