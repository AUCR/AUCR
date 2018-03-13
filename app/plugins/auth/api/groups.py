"""Groups auth plugin api functionality."""
# coding=utf-8
from flask import jsonify, request, url_for
from app import db
from app.plugins.auth.models import Group
from app.plugins.api.routes import api_page
from app.plugins.api.auth import token_auth
from app.plugins.errors.api.errors import bad_request


@api_page.route('/groups/<int:group_id>', methods=['GET'])
@token_auth.login_required
def get_group(group_id):
    """"Return group API call."""
    return jsonify(Group.query.get_or_404(group_id).to_dict())


@api_page.route('/groups', methods=['GET'])
@token_auth.login_required
def get_groups():
    """Return group list API call."""
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Group.to_collection_dict(Group.query, page, per_page, 'api.get_groups')
    return jsonify(data)


@api_page.route('/groups', methods=['POST'])
def create_group() -> object:
    """API create new group call."""
    data = request.get_json() or {}
    if 'group_name' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include group_name, email and password fields')
    if Group.query.filter_by(group_name=data['group_name']).first():
        return bad_request('please use a different group_name')
    if Group.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    group = Group()
    group.from_dict(data, new_group=True)
    db.session.add(group)
    db.session.commit()
    response = jsonify(Group.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_group', id=Group.id)
    return response


@api_page.route('/groups/<int:group_id>', methods=['PUT'])
@token_auth.login_required
def update_group(group_id):
    """API update group call."""
    group = Group.query.get_or_404(group_id)
    data = request.get_json() or {}
    if 'group_name' in data and data['group_name'] != group.group_name and \
            Group.query.filter_by(group_name=data['group_name']).first():
        return bad_request('please use a different group_name')
    if 'email' in data and data['username'] != group.username and \
            Group.query.filter_by(username=data['username']).first():
        return bad_request('please use a different email address')
    Group.from_dict(data, new_group=False)
    db.session.commit()
    return jsonify(Group.to_dict())
