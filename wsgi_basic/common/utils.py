import collections

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
    try:
        # Retrieve the auth context that was prepared by AuthContextMiddleware.
        auth_context = (context['environment']
                        [authorization.AUTH_CONTEXT_ENV])
        return auth_context['token']
    except KeyError:
        LOG.warning("Couldn't find the auth context.")
        raise exception.Unauthorized()


def flatten_dict(d, parent_key=''):
    """Flatten a nested dictionary

    Converts a dictionary with nested values to a single level flat
    dictionary, with dotted notation for each key.

    """
    items = []
    for k, v in d.items():
        new_key = parent_key + '.' + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(list(flatten_dict(v, new_key).items()))
        else:
            items.append((new_key, v))
    return dict(items)

