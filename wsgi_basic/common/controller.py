import functools

from oslo_log import log
from oslo_utils import strutils

from wsgi_basic import exception
from wsgi_basic.common import authorization, wsgi, utils


LOG = log.getLogger(__name__)


class V1Controller(wsgi.Application):
    """V1 Controller"""


def _build_policy_check_credentials(self, action, context, kwargs):
    kwargs_str = ', '.join(['%s=%s' % (k, kwargs[k]) for k in kwargs])
    kwargs_str = strutils.mask_password(kwargs_str)

    LOG.debug('RBAC: Authorizing %(action)s(%(kwargs)s)', {
        'action': action,
        'kwargs': kwargs_str})

    # see if auth context has already been created. If so use it.
    if ('environment' in context and
            authorization.AUTH_CONTEXT_ENV in context['environment']):
        LOG.debug('RBAC: using auth context from the request environment')
        return context['environment'].get(authorization.AUTH_CONTEXT_ENV)

    # There is no current auth context, build it from the incoming token.
    # TODO(morganfainberg): Collapse this logic with AuthContextMiddleware
    # in a sane manner as this just mirrors the logic in AuthContextMiddleware
    try:
        token_ref = self.token_api.get_token(context['token_id'])
    except exception.TokenNotFound:
        LOG.warning('RBAC: Invalid token')
        raise exception.Unauthorized()

    auth_context = token_ref

    return auth_context


def protected(callback=None):
    """Wraps API calls with role based access controls (RBAC).

    This handles both the protection of the API parameters as well as any
    target entities for single-entity API calls.

    More complex API calls (for example that deal with several different
    entities) should pass in a callback function, that will be subsequently
    called to check protection for these multiple entities. This callback
    function should gather the appropriate entities needed and then call
    check_protection() in the V3Controller class.

    """
    def wrapper(f):
        @functools.wraps(f)
        def inner(self, context, *args, **kwargs):
            if 'is_admin' in context and context['is_admin']:
                LOG.warning('RBAC: Bypassing authorization')
            elif callback is not None:
                prep_info = {'f_name': f.__name__,
                             'input_attr': kwargs}
                callback(self, context, prep_info, *args, **kwargs)
            else:
                action = 'wsgi_basic:%s' % f.__name__
                creds = _build_policy_check_credentials(self, action,
                                                        context, kwargs)

                policy_dict = {}

                # Add in the kwargs, which means that any entity provided as a
                # parameter for calls like create and update will be included.
                policy_dict.update(kwargs)
                self.policy_api.enforce(creds,
                                        action,
                                        utils.flatten_dict(policy_dict))
                LOG.debug('RBAC: Authorization granted')
            return f(self, context, *args, **kwargs)
        return inner
    return wrapper
