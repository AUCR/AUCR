"""AUCR auth plugin call utility library."""
# coding=utf-8
from flask import session
from flask_login import current_user
from app.plugins.auth.models import Group, Groups

user_groups_ids = {}


def get_groups():
    """Return group list from database."""
    user_groups_ids["items"] = Group.query.filter_by(username=current_user.id).all()
    user_groups = []
    for items in user_groups_ids["items"]:
        group_object = Groups.query.filter_by(id=items.id).first()
        user_groups.append(group_object.group_name)
    return user_groups


def check_group(group_test):
    """Return a True or False group check."""
    if session is not None:
        test_group = Group.query.filter_by(username=current_user.id).all()
        if test_group is not None:
            for group_items in test_group:
                if group_test == str(group_items.group_name):
                    return True
        else:
            return False
