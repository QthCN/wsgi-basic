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

@dependency.requires('token_provider_api')
@dependency.provider('token_api')
class Manager(manager.Manager):

    driver_namespace = 'wsgi_basic.token.persistence'

    def __init__(self):
        super(Manager, self).__init__(CONF.token.driver)


@six.add_metaclass(abc.ABCMeta)
class Driver(object):
    """Interface description for a Token driver."""

    @abc.abstractmethod
    def get_token(self, token_id):
        """Get a token by id.

        :param token_id: identity of the token
        :type token_id: string
        :returns: token_ref
        :raises: keystone.exception.TokenNotFound

        """
        raise exception.NotImplemented()

    @abc.abstractmethod
    def create_token(self, token_id, data):
        """Create a token by id and data.

        :param token_id: identity of the token
        :type token_id: string
        :param data: dictionary with additional reference information

        ::

            {
                expires=''
                id=token_id,
                user=user_ref,
                tenant=tenant_ref,
                metadata=metadata_ref
            }

        :type data: dict
        :returns: token_ref or None.

        """
        raise exception.NotImplemented()  # pragma: no cover

    @abc.abstractmethod
    def delete_token(self, token_id):
        """Deletes a token by id.

        :param token_id: identity of the token
        :type token_id: string
        :returns: None.
        :raises: keystone.exception.TokenNotFound

        """
        raise exception.NotImplemented()  # pragma: no cover

    @abc.abstractmethod
    def delete_tokens(self, user_id, tenant_id=None, trust_id=None,
                      consumer_id=None):
        """Deletes tokens by user.

        If the tenant_id is not None, only delete the tokens by user id under
        the specified tenant.

        If the trust_id is not None, it will be used to query tokens and the
        user_id will be ignored.

        If the consumer_id is not None, only delete the tokens by consumer id
        that match the specified consumer id.

        :param user_id: identity of user
        :type user_id: string
        :param tenant_id: identity of the tenant
        :type tenant_id: string
        :param trust_id: identity of the trust
        :type trust_id: string
        :param consumer_id: identity of the consumer
        :type consumer_id: string
        :returns: The tokens that have been deleted.
        :raises: keystone.exception.TokenNotFound

        """
        if not CONF.token.revoke_by_id:
            return
        token_list = self._list_tokens(user_id,
                                       tenant_id=tenant_id,
                                       trust_id=trust_id,
                                       consumer_id=consumer_id)

        for token in token_list:
            try:
                self.delete_token(token)
            except exception.NotFound:
                pass
        return token_list

    @abc.abstractmethod
    def _list_tokens(self, user_id, tenant_id=None, trust_id=None,
                     consumer_id=None):
        """Returns a list of current token_id's for a user

        This is effectively a private method only used by the ``delete_tokens``
        method and should not be called by anything outside of the
        ``token_api`` manager or the token driver itself.

        :param user_id: identity of the user
        :type user_id: string
        :param tenant_id: identity of the tenant
        :type tenant_id: string
        :param trust_id: identity of the trust
        :type trust_id: string
        :param consumer_id: identity of the consumer
        :type consumer_id: string
        :returns: list of token_id's

        """
        raise exception.NotImplemented()  # pragma: no cover

    @abc.abstractmethod
    def list_revoked_tokens(self):
        """Returns a list of all revoked tokens

        :returns: list of token_id's

        """
        raise exception.NotImplemented()  # pragma: no cover

    @abc.abstractmethod
    def flush_expired_tokens(self):
        """Archive or delete tokens that have expired.
        """
        raise exception.NotImplemented()  # pragma: no cover