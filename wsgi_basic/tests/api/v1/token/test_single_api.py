import datetime
import json
import time

from wsgi_basic import exception
from wsgi_basic.db.mysql import MYSQL_DATETIME_FMT
from wsgi_basic.tests.base import BaseTestCase
import wsgi_basic.tests.config as config


class TokenSingleAPITest(BaseTestCase):

    def test_create_token_with_right_account(self):
        username = config.USERNAME
        password = config.PASSWORD
        url = "{s}/v1/tokens".format(s=config.TARGET_SERVICE_ADDRESS)
        payload = dict(auth=dict(username=username,
                                 password=password))
        headers = {"Content-Type": "application/json"}
        response = self.http_client._send_request(
            url=url, headers=headers,
            data=payload, method="POST"
        )

        if response.status_code not in (200, 202):
            raise exception.HTTPCodeError(code=response.status_code)

        content = response.content
        try:
            c = json.loads(content)
            if "error" in c:
                raise exception.HTTPContentError(error=c["error"])
        except:
            # response has no content, so code check is enough
            pass

    def test_create_token_with_wrong_account(self):
        username = config.USERNAME
        password = config.PASSWORD + "w"
        url = "{s}/v1/tokens".format(s=config.TARGET_SERVICE_ADDRESS)
        payload = dict(auth=dict(username=username,
                                 password=password))
        headers = {"Content-Type": "application/json"}
        response = self.http_client._send_request(
            url=url, headers=headers,
            data=payload, method="POST"
        )

        content = response.content
        self.assertEqual(response.status_code, 401)
        self.assertIn("error", json.loads(content))

    def test_create_token_with_noexist_user(self):
        username = config.USERNAME + "w"
        password = config.PASSWORD
        url = "{s}/v1/tokens".format(s=config.TARGET_SERVICE_ADDRESS)
        payload = dict(auth=dict(username=username,
                                 password=password))
        headers = {"Content-Type": "application/json"}
        response = self.http_client._send_request(
            url=url, headers=headers,
            data=payload, method="POST"
        )

        content = response.content
        self.assertEqual(response.status_code, 401)
        self.assertIn("error", json.loads(content))

    def test_delete_token(self):
        token = self.http_client.get_v1_token()
        url = "{s}/v1/tokens/{t}".format(s=config.TARGET_SERVICE_ADDRESS,
                                         t=token)
        self.http_client.send_request_with_check(url=url, method="DELETE")
        with self.DB(**self.db_args) as db:
            db.execute("SELECT token_id FROM TOKENS WHERE "
                       "token_id='{id}'".format(id=token))
            data = db.fetchall()
            self.assertEqual(0, len(data))

    def test_get_token(self):
        token = self.http_client.get_v1_token()
        url = "{s}/v1/tokens/{t}".format(s=config.TARGET_SERVICE_ADDRESS,
                                         t=token)
        response = self.http_client.send_request_with_check(url=url,
                                                            method="GET")
        content = json.loads(response.content)
        self.assertEqual(config.ADMIN_USERNAME, content["username"])
        self.assertEqual("admin", content["role"])

    def test_refresh_token_expiration_time(self):
        token = self.http_client.get_v1_token()
        first_expire_time = None
        second_expire_time = None
        url = "{s}/v1/tokens/{t}".format(s=config.TARGET_SERVICE_ADDRESS,
                                         t=token)
        response = self.http_client.send_request_with_check(url=url,
                                                            method="GET")
        with self.DB(**self.db_args) as db:
            db.execute("SELECT expire_time FROM TOKENS WHERE "
                       "token_id='{id}'".format(id=token))
            data = db.fetchall()
            first_expire_time = data[0]["expire_time"]

        sleep_time = 5
        time.sleep(sleep_time)

        url = "{s}/v1/tokens/{t}".format(s=config.TARGET_SERVICE_ADDRESS,
                                         t=token)
        response = self.http_client.send_request_with_check(url=url,
                                                            method="GET")
        with self.DB(**self.db_args) as db:
            db.execute("SELECT expire_time FROM TOKENS WHERE "
                       "token_id='{id}'".format(id=token))
            data = db.fetchall()
            second_expire_time = data[0]["expire_time"]

        time_delta = (second_expire_time - first_expire_time).total_seconds()
        self.assertTrue(time_delta + 1 >= sleep_time, "time delta not good")
