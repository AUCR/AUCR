# coding=utf-8
"""Default unittests to automate functional testing of AUCR code."""
# !/usr/bin/env python
import unittest
from flask import jsonify
from aucr_app import db, aucr_app
from aucr_app.plugins.main import cli
from aucr_app.plugins.auth.models import User
from aucr_app.plugins.auth.auth_globals import AVAILABLE_CHOICES
from aucr_app.plugins.analysis.file.zip import encrypt_zip_file, decrypt_zip_file_map
from aucr_app.plugins.analysis.file.upload import create_upload_file
from aucr_app.plugins.analysis.file.upload import FileUpload
from aucr_app.plugins.tasks.mq import index_mq_aucr_task, get_mq_yaml_configs, index_mq_aucr_report


class UserModelCase(unittest.TestCase):
    """Unittests automated AUCR test case framework."""

    def setUp(self):
        """Set up needed base environment data for unittest."""
        self.app = aucr_app()
        self.app.config['TESTING'] = True
        self.app.config['SECRET_KEY'] = "testing"
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['LANG_VALUE'] = "en"
        self.app.config['SQLALCHEMY_POOL_SIZE'] = None
        self.app.config['SQLALCHEMY_POOL_TIMEOUT'] = None
        cli.register(self.app)
        # Create a default sqlite database for testing
        self.test_user_password = "0Qk9Bata3EO69U5T2qH57lAV1r67Wu"
        test_user = User.__call__(username="test2", email="admin@aucr.io")
        test_user.set_password(self.test_user_password)
        test_user.enable_api()
        db.session.add(test_user)
        db.session.commit()
        self.token = test_user.get_reset_password_token()
        self.test_user = test_user
        self.client = self.app.test_client()

    def test_public_pages(self):
        """Public page unit test function."""

        with self.app.app_context():
            index_mq_aucr_task(rabbit_mq_server=self.app.config['RABBITMQ_SERVER'],
                               task_name=str('73e57937304d89f251e7e540a24b095a'),
                               routing_key="files")
            data_test = get_mq_yaml_configs()
            self.assertEqual(self.client.get('/main/help').status_code, 200)
            self.assertEqual(self.client.get('/main/privacy').status_code, 200)
            self.assertEqual(self.client.get('/main/about_us').status_code, 200)
            index_mq_aucr_report("73e57937304d89f251e7e540a24b095a", str(self.app.config['RABBITMQ_SERVER']), "files")

    def test_auth(self):
        """Authentication unit test function."""
        with self.app.app_context():
            test = AVAILABLE_CHOICES
            test0 = self.client.get('/auth/login')
            test1 = self.client.get('/auth/register')
            test13 = self.client.post('/auth/reset_password_request', data=dict(email="admin3@aucr.io", submit=True),
                                      follow_redirects=True)
            test12 = self.client.post('/auth/register', data=dict(username="testuser1", email="admin+test@aucr.io",
                                                                  password="test", password2="test", submit=True),
                                      follow_redirects=True)
            test234 = self.client.post('/auth/login', data=dict(username="testuser1", password="test", submit=True),
                                     follow_redirects=True)
            test3 = self.client.get('/main/')
            self.assertEqual(self.client.get('/auth/groups', follow_redirects=True).status_code, 200)
            test154 = self.client.get('/auth/logout', follow_redirects=True)
            test2 = self.client.post('/auth/login', data=dict(username="admin", password="aucradmin", submit=True),
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
                                      data=dict(group_name="testgroup", username="admin", submit=True),
                                      follow_redirects=True)
            self.assertEqual(self.client.get('/auth/remove_user_from_group').status_code, 200)
            self.assertEqual(self.client.post('/auth/remove_user_from_group',
                                      data=dict(group_name="testgroup", username="admin", submit=True),
                                      follow_redirects=True).status_code, 200)

            test14 = self.client.post('/auth/edit_profile', data=dict(otp_token_checkbox=True, submit=True),
                                      follow_redirects=True)
            test17 = self.client.get('/auth/reset_password_request')
            test18 = self.client.post('/auth/send_message/admin',
                                      data=dict(recipient_user="admin", message="test", submit=True),
                                      follow_redirects=True)
            test19 = self.client.get('/auth/send_message')
            test30 = self.client.get('/auth/send_message/admin')
            auth = {'Authorization': 'Basic dGVzdDI6MFFrOUJhdGEzRU82OVU1VDJxSDU3bEFWMXI2N1d1'}
            test28 = self.client.post('/auth/tokens',
                                      json={'auth': 'test2:0Qk9Bata3EO69U5T2qH57lAV1r67Wu'},
                                      headers=auth)
            headers = {'Authorization': 'Bearer ' + test28.json["token"]}
            test36 = self.client.post('/analysis/upload_file', data=dict(files="test"), headers=headers)
            test_upload_file = self.client.post('/analysis/upload_file',
                                                data=dict(file=
                                                          ('aucr_app/plugins/main/static/css/main.css',
                                                           'main.css'
                                                           )),
                                                headers=headers)
            self.assertEqual(test_upload_file.status_code, 200)
            tes230 = (self.client.get('/message/_search?=messagesdfsdfsfsdfsdfsf',
                                      headers=headers,
                                      follow_redirects=True))
            test_upload_file_worked = self.client.post('/analysis/upload_file',
                                                       data=dict({'file': (
                                                                      'aucr_app/plugins/main/static/img/apple-icon.png',
                                                                      'apple-icon.png'
                                                                      )}),
                                                       headers=headers)
            self.assertEqual(test_upload_file_worked.status_code, 200)
            test_upload_file_failed = self.client.post('/analysis/upload_file',
                                                       data=dict({'file':
                                                                 ('aucr_app/plugins/main/static/img/apple-icon.png',
                                                                  ''
                                                                  )}),
                                                       headers=headers)
            self.assertEqual(test_upload_file_failed.status_code, 302)
            test39 = self.client.post('/auth/register',
                                      data=dict(email="admin+test@aucr.io",
                                                password="test",
                                                password2="test2",
                                                submit=True),
                                      follow_redirects=True)
            test15 = self.client.get('/auth/logout', follow_redirects=True)
            test38 = self.client.post('/auth/reset_password_request',
                                      data=dict(email="admin@aucr.io",
                                                submit=True),
                                      follow_redirects=True)
            test40 = self.client.get('/auth/reset_password/' + self.token)
            test41 = self.client.post('/auth/reset_password/' + self.token,
                                      data=dict(password="apitest", password2="apitest", submit=True),
                                      follow_redirects=True)

            test23 = self.client.get('/analysis/upload_file', follow_redirects=True)
            test24 = self.client.get('/auth/remove_user_from_group', follow_redirects=True)
            test25 = self.client.get('/api/users/1', headers=headers)
            test26 = self.client.get('/api/groups/1', headers=headers)
            test31 = self.client.get('/api/groups', headers=headers)
            test27 = self.client.get('/api/users', headers=headers)
            test29 = self.client.post('/api/users', json={'username': 'testapi', 'password': 'testing',
                                                          'email': 'test@localhost.local'}, headers=headers)
            test32 = self.client.post('/api/groups', json={'group_name': 'testapi'}, headers=headers)
            test33 = self.client.post('/api/groups', json={'group_name': 'testapi'}, headers=headers)
            test34 = self.client.post('/api/users',
                                      json={'username': 'testapi',
                                            'password': 'testing',
                                            'email': 'test@localhost.local'
                                            },
                                      headers=headers)
            test35 = self.client.post('/api/users',
                                      json={'username': 'testapi',
                                            'password': 'testing',
                                            'email': 'test@localhost.local'
                                            },
                                      headers=headers)
            self.assertEqual(self.client.put('/api/users/1',
                                             json={'username': 'admin',
                                                   'email': 'test232323@localhost.local'
                                                   },
                                      headers=headers).status_code, 200)
            self.assertEqual(self.client.put('/api/groups/1',
                                             json={'name': 'testerer',
                                                   },
                                      headers=headers).status_code, 200)
            self.assertEqual(self.client.post('/auth/remove_user_from_group',
                             data=dict(group_name="admin", admin_user="admin", submit=True),
                             follow_redirects=True).status_code, 200)
            self.assertEqual(self.client.get('/auth/twofactor', follow_redirects=True).status_code, 200)
            self.assertEqual(self.client.get('/auth/qrcode', follow_redirects=True).status_code, 200)
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
            self.assertEqual(test19.status_code, 404)
            test480 = self.client.delete('/auth/tokens',
                                         json={'auth': 'test2:0Qk9Bata3EO69U5T2qH57lAV1r67Wu'},
                                         headers=auth)
            self.assertEqual(test23.status_code, 200)
            self.assertEqual(test24.status_code, 200)
            self.assertEqual(test25.status_code, 200)
            self.assertEqual(test26.status_code, 200)
            self.assertEqual(test27.status_code, 200)
            self.assertEqual(test28.status_code, 200)
            self.assertEqual(test29.status_code, 201)
            self.assertEqual(test30.status_code, 200)
            self.assertEqual(test31.status_code, 200)
            self.assertEqual(test32.status_code, 201)
            self.assertEqual(test33.status_code, 400)
            self.assertEqual(test34.status_code, 400)
            self.assertEqual(test35.status_code, 400)
            self.assertEqual(test36.status_code, 302)
            self.assertEqual(test38.status_code, 200)
            self.assertEqual(test39.status_code, 200)
            self.assertEqual(test40.status_code, 200)
            self.assertEqual(test41.status_code, 200)

    def test_zip_encrypt(self):
        """Return result of zip file function."""
        encrypt_zip_file("infected", "test.zip", ["aucr_app/plugins/main/static/img/loading.gif"])
        test_file = decrypt_zip_file_map(str(self.app.config["TMP_FILE_FOLDER"] + "/test.zip"), "infected")
        test_result = create_upload_file(test_file, str(self.app.config["TMP_FILE_FOLDER"]))
        self.assertEqual(jsonify(FileUpload.query.get_or_404(1).to_dict()).status_code, 200)
        self.assertEqual("73e57937304d89f251e7e540a24b095a", test_result)

    def tearDown(self):
        """Destroy base environment data for unittests."""
        # Drop the database
        db.drop_all()
        db.session.remove()


if __name__ == '__main__':
    unittest.main(verbosity=2)