import json

from wsgi_basic import exception
from wsgi_basic.tests.base import BaseTestCase
import wsgi_basic.tests.config as config


class UserSingleAPITest(BaseTestCase):

    def create_user(self, username, password, role):
        url = "{s}/v1/users".format(s=config.TARGET_SERVICE_ADDRESS)
        payload = dict(username=username,
                       password=password,
                       role=role)
        response = self.http_client.send_request_with_check(
            url=url,
            data=payload,
            method="POST"
        )
        return response

    def delete_user(self, user_id):
        url = "{s}/v1/users/{i}".format(s=config.TARGET_SERVICE_ADDRESS,
                                        i=user_id)
        response = self.http_client.send_request_with_check(
            url=url,
            method="DELETE"
        )
        return response

    def test_create_user(self):
        username = "create_user_user"
        password = "password"
        role = "user"
        response = self.create_user(username, password, role)
        content = json.loads(response.content)
        self.assertEqual(username, content["name"])
        self.assertEqual(role, content["role"])
        self.delete_user(content["user_id"])

    def test_delete_user(self):
        username = "delete_user_user"
        password = "password"
        role = "user"
        response = self.create_user(username, password, role)
        content = json.loads(response.content)
        self.delete_user(content["user_id"])
        with self.DB(**self.db_args) as db:
            db.execute("SELECT id FROM USERS WHERE id='i'".format(
                i=content["user_id"]
            ))
            data = db.fetchall()
            self.assertEqual(0, len(data))

    def test_get_user(self):
        username = "get_user_user"
        password = "password"
        role = "user"
        response = self.create_user(username, password, role)
        content = json.loads(response.content)
        url = "{s}/v1/users/{i}".format(s=config.TARGET_SERVICE_ADDRESS,
                                        i=content["user_id"])
        response = self.http_client.send_request(url=url, method="GET")
        data = json.loads(response.content)
        self.assertEqual(content["user_id"], data["user_id"])
        self.assertEqual(role, data["role"])
        self.assertEqual(username, data["name"])
        self.delete_user(content["user_id"])

    def test_update_user(self):
        username = "update_user_user"
        password = "password"
        role = "user"
        response = self.create_user(username, password, role)
        content = json.loads(response.content)
        user_id = content["user_id"]
        self.assertEqual(role, content["role"])
        new_password = "new_password"
        url = "{s}/v1/users/{i}".format(s=config.TARGET_SERVICE_ADDRESS,
                                        i=content["user_id"])
        payload = dict(password=new_password)
        response = self.http_client.send_request_with_check(url, method="PUT",
                                                            data=payload)
        content = json.loads(response.content)
        self.assertEqual(username, content["name"])
        self.assertEqual(role, content["role"])
        self.assertEqual(user_id, content["user_id"])
        token = self.http_client.get_v1_token(username, password)
        self.assertEqual(token, None)
        token = self.http_client.get_v1_token(username, new_password)
        self.assertNotEqual(token, None)
        self.delete_user(user_id)
