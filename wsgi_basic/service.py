import functools
import sys

from oslo_config import cfg
from oslo_log import log
from paste import deploy
import routes

from wsgi_basic import controllers
from wsgi_basic import routers
from wsgi_basic.common import wsgi
from wsgi_basic.token import routers as token_routers


CONF = cfg.CONF

LOG = log.getLogger(__name__)


def loadapp(conf, name):
    # NOTE(blk-u): Save the application being loaded in the controllers module.
    # This is similar to how public_app_factory() and v3_app_factory()
    # register the version with the controllers module.
    controllers.latest_app = deploy.loadapp(conf, name=name)
    return controllers.latest_app


def fail_gracefully(f):
    """Logs exceptions and aborts."""
    @functools.wraps(f)
    def wrapper(*args, **kw):
        try:
            return f(*args, **kw)
        except Exception as e:
            LOG.debug(e, exc_info=True)

            # exception message is printed to all logs
            LOG.critical(e)
            sys.exit(1)

    return wrapper


@fail_gracefully
def public_app_factory(global_conf, **local_conf):
    return wsgi.ComposingRouter(routes.Mapper(),
                                [token_routers.Router(),
                                 routers.Versions('public')])


@fail_gracefully
def public_version_app_factory(global_conf, **local_conf):
    return wsgi.ComposingRouter(routes.Mapper(),
                                [routers.Versions('public')])

