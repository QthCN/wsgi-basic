import abc
import copy

from oslo_config import cfg
from oslo_log import log
import six

from wsgi_basic import exception
from wsgi_basic.common import dependency
from wsgi_basic.common import manager


CONF = cfg.CONF
LOG = log.getLogger(__name__)

@dependency.provider('token_api')
class Manager(manager.Manager):

    driver_namespace = 'wsgi_basic.token.persistence'

    def __init__(self):
        super(Manager, self).__init__(CONF.token.driver)


@six.add_metaclass(abc.ABCMeta)
class Driver(object):
    """Interface description for a Token driver."""

    @abc.abstractmethod
    def create_token(self, token_id, data):
        raise exception.NotImplemented()

    @abc.abstractmethod
    def delete_token(self, token_id):
        raise exception.NotImplemented()

    @abc.abstractmethod
    def get_token(self, token_id):
        raise exception.NotImplemented()

    @abc.abstractmethod
    def clear_expired_tokens(self):
        raise exception.NotImplemented()
