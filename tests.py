# coding=utf-8
"""Default unittests to automate functional testing of AUCR code."""
# !/usr/bin/env python
import unittest
from aucr_app import db, aucr_app
from aucr_app.plugins.auth.models import User
from aucr_app.plugins.analysis.file.zip import encrypt_zip_file, decrypt_zip_file_map
from aucr_app.plugins.analysis.file.upload import create_upload_file


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
            test16 = self.client.post('/auth/reset_password_request', data=dict(email="admin@aucr.io", submit=True),
                                      follow_redirects=True)
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
            test17 = self.client.get('/auth/reset_password_request')
            test18 = self.client.post('/auth/send_message', data=dict(recipient_user="admin", message="test", submit=True),
                                      follow_redirects=True)
            test19 = self.client.get('/auth/send_message')
            test15 = self.client.get('/auth/logout', follow_redirects=True)
            test20 = self.client.get('/main/help')
            test21 = self.client.get('/main/privacy')
            test22 = self.client.get('/main/about_us')
            test23 = self.client.get('/analysis/upload_file', follow_redirects=True)
            test24 = self.client.get('/auth/remove_user_from_group', follow_redirects=True)

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
            self.assertEqual(test16.status_code, 200)
            self.assertTrue(test17)
            self.assertTrue(test18)
            self.assertTrue(test19)
            self.assertEqual(test20.status_code, 200)
            self.assertEqual(test21.status_code, 200)
            self.assertEqual(test22.status_code, 200)
            self.assertEqual(test23.status_code, 200)
            self.assertEqual(test24.status_code, 200)

    def test_zip_encrypt(self):
        encrypt_zip_file("infected", "test.zip", ["aucr_app/plugins/main/static/img/loading.gif"])
        test_file = decrypt_zip_file_map("upload/test.zip", "infected")
        test_result = create_upload_file(test_file, "upload")
        self.assertEqual("73e57937304d89f251e7e540a24b095a", test_result)


if __name__ == '__main__':
    unittest.main(verbosity=2)
