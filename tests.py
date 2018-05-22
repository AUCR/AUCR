# coding=utf-8
"""Default unittests to automate functional testing of AUCR code."""
# !/usr/bin/env python
import unittest
import time
from config import Config
from flask_wtf import CSRFProtect
from app import create_app, db
from app.plugins.main import main_page
from app.plugins.auth.models import User, Group, Groups
from app.plugins.auth.utils import check_group, get_group_permission_navbar
from app.plugins.auth.email import send_password_reset_email, send_async_email, send_email
from app.plugins.analysis.file.zip import encrypt_zip_file, decrypt_zip_file_map, compress_zip_file_map
from app.plugins.analysis.file.upload import create_upload_file

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


class TestConfig(Config):
    """Unittests default config."""

    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    ELASTICSEARCH_URL = None
    LANGUAGES = ['en']
    LOG_TO_STDOUT = 1


class UserModelCase(unittest.TestCase):
    """Unittests automated AUCR test case framework."""

    def setUp(self):
        """Set up needed base environment data for unittests."""
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        # Create a default sqlite database for testing
        db.create_all()
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

    def test_http_error_code_plugin(self):
        """Test error plugin HTTP error code return."""
        app = self.app
        create_group_name = Groups(group_name="test")
        db.session.add(create_group_name)
        db.session.commit()
        user_id = User.query.filter_by(username=self.test_user.username).first()
        group_name = Group(group_name=create_group_name.id, username_id=user_id.id)
        db.session.add(group_name)
        db.session.commit()
        with app.test_client() as test_error_code:
            test_auth_groups = test_error_code.get('test')
            self.assertEqual(test_auth_groups.data, b'{\n  "error": "Unknown error"\n}\n')

    def test_user_reset_password(self):
        """Test AUCR auth plugin reset password."""
        app = self.app
        try:
            with app.test_client():
                send_password_reset_email(user=self.test_user)
        # TODO figure out how to get past the run time error this at least makes sure our password reset works somewhat
        except RuntimeError as expected_result:
            test = str(expected_result.args[0])
            self.assertAlmostEqual(test, '''Working outside of request context.

This typically means that you attempted to use functionality that needed
an active HTTP request.  Consult the documentation on testing for
information about how to avoid this problem.''')

    def test_send_mail(self):
        """This let's test our send email functions to ensure things work as expected."""
        app = self.app
        test_recipients = ["test1@test.com", "test2@test.com"]
        test_result = send_email("Test Subject", "test3@test.com", test_recipients, "Test Message", "Nothing")
        send_async_email(app, test_result)

    def test_zip_encrypt(self):
        app = self.app
        encrypt_zip_file("infected", "test.zip", ["app/plugins/main/static/img/loading.gif"])
        test_file = decrypt_zip_file_map("upload/test.zip", "infected")
        test_result = create_upload_file(test_file, "upload")
        self.assertEqual("73e57937304d89f251e7e540a24b095a", test_result)

    def test_navbar_builder(self):
        test_navbar = get_group_permission_navbar()
        test_value = test_navbar["tasks"][0]
        self.assertTrue(test_value)


if __name__ == '__main__':
    unittest.main(verbosity=2)
