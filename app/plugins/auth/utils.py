"""AUCR auth plugin call utility library."""
# coding=utf-8
import glob
import logging
from flask import session
from flask_login import current_user
from app.plugins.auth.models import Group, Groups
from yaml_info.yamlinfo import YamlInfo

user_groups_ids = {}


def get_groups():
    """Return group list from database."""
    user_groups_ids["items"] = Group.query.filter_by(username_id=current_user.id).all()
    user_groups = []
    for items in user_groups_ids["items"]:
        group_object = Groups.query.filter_by(id=items.group_name).first()
        user_groups.append(group_object.group_name)
    return user_groups


def check_group(group_test):
    """Return a True or False group check."""
    if session is not None:
        test_group_id = Group.query.filter_by(username_id=current_user.id).all()
        test_group = Groups.query.filter_by(id=test_group_id.id).all()
        if test_group:
            for group_items in test_group:
                if group_test == str(group_items.group_name):
                    return True
        else:
            return False


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
    tasks_list = []
    analysis_list = []
    main_list = []
    reports_list = []
    for items in user_groups_ids["items"]:
        group_object = Groups.query.filter_by(id=items.group_name).first()
        for filename in glob.iglob('app/plugins/**/navbar.yml', recursive=True):
            menu_links = YamlInfo(filename, "none", "none")
            run = menu_links.get()
            tasks_result_list = generate_navbar_list_item("tasks", run, group_object.group_name, tasks_list)
            if tasks_result_list:
                tasks_list = tasks_result_list
            analysis_result_list = generate_navbar_list_item("analysis", run, group_object.group_name, analysis_list)
            if analysis_result_list:
                analysis_list = analysis_result_list
            reports_result_list = generate_navbar_list_item("reports", run, group_object.group_name, reports_list)
            if reports_result_list:
                reports_list = reports_result_list
            main_result_list = generate_navbar_list_item("main", run, group_object.group_name, main_list)
            if main_result_list:
                main_list = main_result_list
    user_groups_links["tasks"] = tasks_list
    user_groups_links["reports"] = reports_list
    user_groups_links["analysis"] = analysis_list
    user_groups_links["main"] = main_list
    return user_groups_links
