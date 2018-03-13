"""Auth routes manages all basic authentication."""
# coding=utf-8
from flask import Blueprint, jsonify
from app import db
from flask import g
from app.plugins.api.auth import token_auth, basic_auth

api_page = Blueprint('api', __name__, template_folder='templates')


@api_page.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    """Get user token."""
    token = g.current_user.get_token()
    db.session.commit()
    return jsonify({'token': token})


@api_page.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    """Revoke user token."""
    g.current_user.revoke_token()
    db.session.commit()
    return '', 204
