"""AUCR main auth plugin api features."""
# coding=utf-8
from flask import jsonify, request, url_for
from aucr_app import db
from aucr_app.plugins.auth.models import User
from aucr_app.plugins.api.routes import api_page
from aucr_app.plugins.api.auth import token_auth
from aucr_app.plugins.errors.api.errors import bad_request


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
    data = User.to_collection_dict(User.query, page, per_page, 'api.get_users')
    return jsonify(data)


@api_page.route('/users', methods=['POST'])
def create_user():
    """API Create new user."""
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include username, email and password fields')
    if User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user = User()
    user.from_dict(data, new_user=True)
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
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
