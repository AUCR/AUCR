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



csrf = CSRFProtect()


@main_page.route('/test', methods=['GET'])
@csrf.exempt
def test_auth():
    """Test group permissions."""
    try:
        if check_group("test"):
            return "403"
    except AttributeError:
        return "403"


class UserModelCase(unittest.TestCase):
    """Unittests automated AUCR test case framework."""

    def setUp(self):
        """Set up needed base environment data for unittests."""
        self.app = aucr_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        # Create a default sqlite database for testing
        self.test_user_password = "0Qk9Bata3EO69U5T2qH57lAV1r67Wu"
        test_user = User.__call__(username="test2", email="test2@example.com")
        test_user.set_password(self.test_user_password)
        db.session.add(test_user)
        db.session.commit()
        csrf.init_app(self.app)
        self.csrf = CSRFProtect(self.app)
        self.test_user = test_user

    def tearDown(self):
        """Destroy base environment data for unittests."""
        db.session.remove()
        # Drop the database
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        """Test auth plugin password hashing."""
        test_password_user = User.__call__(username="test1")
        # These are randomly generated passwords for a longer complexity check to ensure this works as expected
        test_password_user.set_password(self.test_user_password)
        self.assertFalse(test_password_user.check_password('H2Y5Xns732tx27DyL509910dkJ8lSL'))
        self.assertTrue(test_password_user.check_password(self.test_user_password))

    def test_avatar(self):
        """Test avatar creation for users."""
        # Hard coded because we expect this to be the results
        self.assertEqual(self.test_user.avatar(128),
                         'https://www.gravatar.com/avatar/43b05f394d5611c54a1a9e8e20baee21?d=identicon&s=128')

    def test_user_registration_and_auth(self):
        """Test user auth plugin user registration."""
        tests_errors_user = User.query.filter_by(username="test2").first()
        if tests_errors_user is None or not tests_errors_user.check_password(self.test_user_password):
            assert b'Invalid username or password'
        self.assertTrue(tests_errors_user)


if __name__ == '__main__':
    unittest.main(verbosity=2)
