"""AUCR auth plugin call utility library."""
# coding=utf-8
import glob
from flask import session
from flask_login import current_user
from aucr_app.plugins.auth.models import Group, Groups
from yaml_info.yamlinfo import YamlInfo

user_groups_ids = {}


def get_groups():
    """Return group list from database."""
    user_groups_ids["items"] = Group.query.filter_by(username_id=current_user.id).all()
    user_groups = []
    for items in user_groups_ids["items"]:
        group_object = Groups.query.filter_by(id=items.groups_id).first()
        user_groups.append(group_object.name)
    return user_groups


def generate_navbar_list_item(item, navbar_dict, group_name, generated_navbar_list):
    """Loop generate navbar list."""
    try:
        if item in navbar_dict:
            run_item_list = navbar_dict[item]
            for run_items in run_item_list[group_name]:
                generated_navbar_list.append(run_items)
        return generated_navbar_list
    except KeyError:
        return False


def get_group_permission_navbar():
    """Return group nav list from database."""
    if current_user:
        current_user_id = current_user.id
    else:
        current_user_id = 1
    user_groups_ids["items"] = Group.query.filter_by(username_id=current_user_id).all()
    user_groups_links = {}
    main_list = []
    for items in user_groups_ids["items"]:
        group_object = Groups.query.filter_by(id=items.groups_id).first()
        for filename in glob.iglob('aucr_app/plugins/**/navbar.yml', recursive=True):
            menu_links = YamlInfo(filename, "none", "none")
            run = menu_links.get()
            main_result_list = generate_navbar_list_item("main", run, group_object.name, main_list)
            if main_result_list:
                main_list = main_result_list
    # Used to make sure empty lists are not populating the navbar dictionary
    if main_list:
        user_groups_links["main"] = main_list
    return user_groups_links
