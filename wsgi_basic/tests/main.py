import ConfigParser

import nose

import wsgi_basic.tests.config as config


config_file_path = "etc/test.ini"


def init_config():
    cf = ConfigParser.ConfigParser()
    cf.read(config_file_path)
    config.TARGET_SERVICE_ADDRESS = cf.get("test", "TARGET_SERVICE_ADDRESS")
    config.ADMIN_USERNAME = cf.get("test", "ADMIN_USERNAME")
    config.ADMIN_PASSWORD = cf.get("test", "ADMIN_PASSWORD")
    config.USERNAME = cf.get("test", "USERNAME")
    config.PASSWORD = cf.get("test", "PASSWORD")
    config.MYSQL_HOST = cf.get("test", "MYSQL_HOST")
    config.MYSQL_USER = cf.get("test", "MYSQL_USER")
    config.MYSQL_PASSWORD = cf.get("test", "MYSQL_PASSWORD")
    config.MYSQL_PORT = int(cf.get("test", "MYSQL_PORT"))
    config.MYSQL_SCEHMA = cf.get("test", "MYSQL_SCEHMA")


def main():
    init_config()
    nose.main()


if __name__ == "__main__":
    main()

