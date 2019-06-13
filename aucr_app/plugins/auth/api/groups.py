"""Groups auth plugin api functionality."""
# coding=utf-8
from flask import jsonify, request, url_for
from aucr_app import db
from aucr_app.plugins.auth.models import Group, Groups
from aucr_app.plugins.api.routes import api_page
from aucr_app.plugins.api.auth import token_auth
from aucr_app.plugins.errors.api.errors import bad_request


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
@token_auth.login_required
def create_group() -> object:
    """API create new group call."""
    data = request.get_json() or {}
    if 'group_name' not in data:
        return bad_request('must include group_name field')
    if Groups.query.filter_by(name=data['group_name']).first():
        return bad_request('please use a different group_name')
    group = Groups(name=data['group_name'])
    group.from_dict(data)
    db.session.add(group)
    db.session.commit()
    response = jsonify(group.to_dict())
    response.status_code = 201
    return response


@api_page.route('/groups/<int:group_id>', methods=['PUT'])
@token_auth.login_required
def update_group(group_id):
    """API update group call."""
    group = Groups.query.get_or_404(group_id)
    data = request.get_json() or {}
    if 'name' in data and data['name'] != group.name and \
            Groups.query.filter_by(name=data['name']).first():
        return bad_request('please use a different group_name')
    group.from_dict(data)
    db.session.commit()
    return jsonify(group.to_dict())
