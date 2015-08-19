from oslo_log import log
from oslo_serialization import jsonutils

from wsgi_basic import exception
from wsgi_basic.common import authorization


LOG = log.getLogger(__name__)


class SmarterEncoder(jsonutils.json.JSONEncoder):
    """Help for JSON encoding dict-like objects."""
    def default(self, obj):
        if not isinstance(obj, dict) and hasattr(obj, 'iteritems'):
            return dict(obj.iteritems())
        return super(SmarterEncoder, self).default(obj)

def get_token_ref(context):
    """Retrieves KeystoneToken object from the auth context and returns it.

    :param dict context: The request context.
    :raises: exception.Unauthorized if auth context cannot be found.
    :returns: The KeystoneToken object.
    """
    try:
        # Retrieve the auth context that was prepared by AuthContextMiddleware.
        auth_context = (context['environment']
                        [authorization.AUTH_CONTEXT_ENV])
        return auth_context['token']
    except KeyError:
        LOG.warning("Couldn't find the auth context.")
        raise exception.Unauthorized()

