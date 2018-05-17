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


def get_group_permission_navbar():
    """Return group nav list from database."""
    user_groups_ids["items"] = Group.query.filter_by(username=current_user.id).all()
    user_groups_links = {}
    tasks_list = []
    analysis_list = []
    reports_list = []
    for items in user_groups_ids["items"]:
        group_object = Groups.query.filter_by(id=items.group_name).first()

        for filename in glob.iglob('app/plugins/**/navbar.yml', recursive=True):
            menu_links = YamlInfo(filename, "none", "none")
            run = menu_links.get()
            try:
                if "tasks" in run:
                    run_tasks_list = run["tasks"]
                    for run_items in run_tasks_list[group_object.group_name]:
                        tasks_list.append(run_items)
                if "analysis" in run:
                    run_analysis_list = run["analysis"]
                    for analysis_items in run_analysis_list:
                        analysis_list.append(analysis_items)
                if "reports" in run:
                    run_analysis_list = run["reports"]
                    if run_analysis_list[group_object.group_name]:
                        for report_items in run["reports"][group_object.group_name]:
                            reports_list.append(report_items)
            except KeyError as k:
                logging.info("Key not found " + str(k))
                pass
    user_groups_links["tasks"] = tasks_list
    user_groups_links["reports"] = reports_list
    user_groups_links["analysis"] = analysis_list
    return user_groups_links
