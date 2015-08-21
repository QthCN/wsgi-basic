import unittest

from wsgi_basic.db.mysql import DB
from wsgi_basic.tests.config import *
from wsgi_basic.tests.utils import HTTPClient


class BaseTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        self.http_client = HTTPClient()
        self.db_args = dict(host=MYSQL_HOST, port=MYSQL_PORT,
                            username=MYSQL_USER, password=MYSQL_PASSWORD,
                            schema=MYSQL_SCEHMA)
        self.DB = DB
        super(BaseTestCase, self).__init__(*args, **kwargs)
