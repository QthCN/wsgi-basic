import MySQLdb
from oslo_config import cfg
from oslo_log import log


CONF = cfg.CONF

LOG = log.getLogger(__name__)


MYSQL_DATETIME_FMT = "%Y-%m-%d %H:%M:%S"


class DB(object):

    def __init__(self, host=None, port=None, username=None,
                 password=None, schema=None):
        self.host = host or CONF.mysql.host
        self.port = port or CONF.mysql.port
        self.username = username or CONF.mysql.username
        self.password = password or CONF.mysql.password
        self.schema = schema or CONF.mysql.schema

    def __enter__(self):
        self.conn = None
        self.cursor = None
        try:
            self.conn = MySQLdb.connect(host=self.host, port=self.port,
                                        user=self.username,
                                        passwd=self.password,
                                        db=self.schema)
            self.conn.autocommit(False)
            self.cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
        except Exception as e:
            LOG.exception(e)
        finally:
            return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if self.conn:
                self.conn.commit()
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
        except Exception as e:
            LOG.exception(e)

