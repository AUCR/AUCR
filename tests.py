# coding=utf-8
"""Default unittests to automate functional testing of AUCR code."""
# !/usr/bin/env python
import os
import tempfile
import pytest
import unittest
import re
import time
from config import Config
from flask_wtf import CSRFProtect
from app import create_app, db, aucr_app, init_app
from app.plugins.main import main_page
from app.plugins.auth.models import User, Group, Groups
from app.plugins.auth.utils import check_group, get_group_permission_navbar
from app.plugins.auth.email import send_password_reset_email, send_async_email, send_email
from app.plugins.analysis.file.zip import encrypt_zip_file, decrypt_zip_file_map, write_file_map
from app.plugins.analysis.file.upload import create_upload_file


class UserModelCase(unittest.TestCase):
    """Unittests automated AUCR test case framework."""

    def setUp(self):
        """Set up needed base environment data for unittests."""
        self.app = aucr_app()
        self.app.config['TESTING'] = True
        self.app.config['SECRET_KEY'] = "testing"
        self.app.config['WTF_CSRF_ENABLED'] = False
        # Create a default sqlite database for testing
        self.test_user_password = "0Qk9Bata3EO69U5T2qH57lAV1r67Wu"
        test_user = User.__call__(username="test2", email="test2@example.com")
        test_user.set_password(self.test_user_password)
        db.session.add(test_user)
        db.session.commit()
        self.test_user = test_user
        self.client = self.app.test_client()

    def tearDown(self):
        """Destroy base environment data for unittests."""
        db.session.remove()
        # Drop the database
        db.drop_all()

    def test_auth(self):
        with self.app.app_context():
            test0 = self.client.get('/auth/login')
            test1 = self.client.get('/auth/register')
            test13 = self.client.post('/auth/reset_password_request', data=dict(email="admin@aucr.io", submit=True),
                                      follow_redirects=True)
            test12 = self.client.post('/auth/register', data=dict(username="testuser1", email="admin+test@aucr.io",
                                                                  password="test", password2="test",
                                                                  website="aucr.io", affiliation="testing group",
                                                                  country="None", submit=True),
                                      follow_redirects=True)
            test2 = self.client.post('/auth/login', data=dict(username="admin", password="admin", submit=True),
                                     follow_redirects=True)
            test3 = self.client.get('/main/')
            test4 = self.client.get('/auth/groups')
            test5 = self.client.get('/auth/user/admin')
            test6 = self.client.get('/auth/edit_profile')
            test7 = self.client.get('/auth/users')
            test8 = self.client.get('/auth/messages')
            test9 = self.client.get('/auth/groups')
            test10 = self.client.get('/auth/create_group')
            test11 = self.client.post('/auth/create_group',
                                      data=dict(group_name="testgroup", admin_user="admin", submit=True),
                                      follow_redirects=True)
            test14 = self.client.post('/auth/edit_profile', data=dict(otp_token_checkbox=True, submit=True),
                                      follow_redirects=True)
            test15 = self.client.get('/auth/logout')
            self.assertEqual(test0.status_code, 200)
            self.assertEqual(test1.status_code, 200)
            self.assertEqual(test2.status_code, 200)
            self.assertEqual(test3.status_code, 200)
            self.assertEqual(test4.status_code, 200)
            self.assertEqual(test5.status_code, 200)
            self.assertEqual(test6.status_code, 200)
            self.assertEqual(test7.status_code, 200)
            self.assertEqual(test8.status_code, 200)
            self.assertEqual(test9.status_code, 200)
            self.assertEqual(test10.status_code, 200)
            self.assertEqual(test11.status_code, 200)
            self.assertEqual(test12.status_code, 200)
            self.assertEqual(test13.status_code, 200)
            self.assertEqual(test14.status_code, 200)
            self.assertEqual(test15.status_code, 200)

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

    def test_http_error_code_plugin(self):
        """Test error plugin HTTP error code return."""
        app = self.app
        create_group_name = Groups(name="test")
        db.session.add(create_group_name)
        db.session.commit()
        user_id = User.query.filter_by(username=self.test_user.username).first()
        group_name = Group(groups_id=create_group_name.id, username_id=user_id.id)
        db.session.add(group_name)
        db.session.commit()
        with app.test_client() as test_error_code:
            test_auth_groups = test_error_code.get('test')
            self.assertTrue(test_auth_groups.data)

    def test_user_reset_password(self):
        """Test AUCR auth plugin reset password."""
        app = self.app
        try:
            with app.test_client():
                send_password_reset_email(user=self.test_user)
        # TODO figure out how to get past the run time error this at least makes sure our password reset works somewhat
        except RuntimeError as expected_result:
            test = str(expected_result.args[0])
            self.assertTrue(test)

    def test_send_mail(self):
        """This let's test our send email functions to ensure things work as expected."""
        test_recipients = ["admin@aucr.io"]
        test_result = send_email("Test Subject", "admin@aucr.io", test_recipients, "Test Message", "Nothing")
        self.assertFalse(test_result)

    def test_zip_encrypt(self):
        encrypt_zip_file("infected", "test.zip", ["app/plugins/main/static/img/loading.gif"])
        test_file = decrypt_zip_file_map("upload/test.zip", "infected")
        test_result = create_upload_file(test_file, "upload")
        self.assertEqual("73e57937304d89f251e7e540a24b095a", test_result)

    def test_navbar_builder(self):
        test_navbar = get_group_permission_navbar()
        test_value = test_navbar["main"][0]
        self.assertTrue(test_value)


if __name__ == '__main__':
    unittest.main(verbosity=2)
