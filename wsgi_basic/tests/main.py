import nose

import wsgi_basic.tests.config as config
from wsgi_basic.tests.utils import  HTTPClient


def main(target_address="http://127.0.0.1:5000", admin_username="admin",
         admin_password="password", username="user", password="password",
         mysql_host="127.0.0.1", mysql_port=3306, mysql_user="root",
         mysql_password="rootroot", mysql_schema="wsgi_basic"):
    config.TARGET_SERVICE_ADDRESS = target_address
    config.ADMIN_USERNAME = admin_username
    config.ADMIN_PASSWORD = admin_password
    config.USERNAME = username
    config.PASSWORD = password
    config.MYSQL_HOST = mysql_host
    config.MYSQL_USER = mysql_user
    config.MYSQL_PASSWORD = mysql_password
    config.MYSQL_PORT = mysql_port
    config.MYSQL_SCEHMA = mysql_schema
    nose.main()


if __name__ == "__main__":
    main()

