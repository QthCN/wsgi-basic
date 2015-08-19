import abc

from oslo_config import cfg
from oslo_log import log
import six

from wsgi_basic import exception
from wsgi_basic.common import dependency
from wsgi_basic.common import manager


CONF = cfg.CONF
LOG = log.getLogger(__name__)


@dependency.provider('token_provider_api')
class Manager(manager.Manager):
    """Default pivot point for the token provider backend. """

    driver_namespace = 'wsgi_basic.token.provider'

    def __init__(self):
        super(Manager, self).__init__(CONF.token.provider)


@six.add_metaclass(abc.ABCMeta)
class Driver(object):
    """Interface description for a Token provider."""

    @abc.abstractmethod
    def get_token_id(self, token_data):
        """Determine if the token should be persisted.

        If the token provider requires that the token be persisted to a
        backend this should return True, otherwise return False.

        """
        raise exception.NotImplemented()