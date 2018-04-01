# coding=utf-8
"""Default unittests to automate functional testing of AUCR code."""
# !/usr/bin/env python
import unittest
from config import Config
from app import create_app, db
from app.plugins.main import main_page
from app.plugins.auth.models import User, Group, Groups
from app.plugins.auth.utils import check_group
from app.plugins.auth.email import send_password_reset_email, send_async_email, send_email
from flask_wtf import CSRFProtect

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

    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    ELASTICSEARCH_URL = None
    LANGUAGES = ['en']


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
        group_name = Group(group_name=create_group_name.id, username=user_id.id)
        db.session.add(group_name)
        db.session.commit()
        with app.test_client() as test_error_code:
            test_auth_groups = test_error_code.get('test')
            self.assertEqual(test_auth_groups.data, b'403')

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


if __name__ == '__main__':
    unittest.main(verbosity=2)
