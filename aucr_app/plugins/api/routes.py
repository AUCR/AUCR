"""Auth routes manages all basic authentication."""
# coding=utf-8
from flask import Blueprint, jsonify, request
from aucr_app import db
from flask import g
from aucr_app.plugins.api.auth import basic_auth

api_page = Blueprint('api', __name__, template_folder='templates')


@api_page.route('/tokens', methods=['POST', 'DELETE'])
@basic_auth.login_required
def get_token():
    """Get user token."""
    if request.method == "POST":
        if g.current_user.api_enabled:
            token = g.current_user.get_token()
            db.session.commit()
            return jsonify({'token': token})
        else:
            return jsonify({'error': "No API access for your account."})
    elif request.method == "DELETE":
        g.current_user.revoke_token()
        db.session.commit()
        return '', 204
    else:
        return jsonify({'error': "Not a proper request."})
