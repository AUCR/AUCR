# coding=utf-8
"""Default unittests to automate functional testing of AUCR code."""
# !/usr/bin/env python
import os
import tempfile
import pytest
import unittest
import time
from config import Config
from flask_wtf import CSRFProtect
from app import create_app, db, aucr_app, init_app
from app.plugins.main import main_page
from app.plugins.auth.models import User, Group, Groups
from app.plugins.auth.utils import check_group, get_group_permission_navbar
from app.plugins.auth.email import send_password_reset_email, send_async_email, send_email
from app.plugins.analysis.file.zip import encrypt_zip_file, decrypt_zip_file_map, compress_zip_file_map
from app.plugins.analysis.file.upload import create_upload_file


@pytest.fixture
def client():
    aucr = create_app()
    db_fd, aucr.config['DATABASE'] = tempfile.mkstemp()
    aucr.config['TESTING'] = True
    client = aucr.test_client()

    with aucr.app_context():
        init_app(aucr)

    yield client
    os.close(db_fd)


def test_main_route(client):
    """Start with a blank database."""

    rv = client.get('/main/')
    assert 302 == rv.status_code


def test_password_hashing(client):
    """Test auth plugin password hashing."""
    test_password_user = User.__call__(username="test1")
    # These are randomly generated passwords for a longer complexity check to ensure this works as expected
    test_password_user.set_password("0Qk9Bata3EO69U5T2qH57lAV1r67Wu")
    assert not test_password_user.check_password("wrong")
    assert test_password_user.check_password("0Qk9Bata3EO69U5T2qH57lAV1r67Wu")


def test_login(client):
    test = client.get('/auth/login')
    token = b'IjY0YmZiZTM5ZTQwOThhMmYwYWVhYmI1NGE4ZTg4ZTgzMTJiZmNlNTYi.DeWf1A.3MhxY9anNaUwgn2BTWmKCEDGDtk'
    test2 = client.post('/auth/login', data=dict(username="admin", password="admin", token=token, submit=True), follow_redirects=True)
    test3 = client.get('/main/')
    return test


def test_logout(client):
    return client.get('/auth/logout', follow_redirects=True)
