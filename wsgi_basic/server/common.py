from oslo_config import cfg

from wsgi_basic import config
from wsgi_basic.server import backends
from wsgi_basic.common import dependency


CONF = cfg.CONF


def configure(version=None, config_files=None,
              project="",
              pre_setup_logging_fn=lambda: None):
    config.configure()
    config.set_default_for_default_log_levels()

    CONF(project=project, version=version,
         default_config_files=config_files)

    pre_setup_logging_fn()
    config.setup_logging(project=project)


def setup_backends(load_extra_backends_fn=lambda: {},
                   startup_application_fn=lambda: None):
    drivers = backends.load_backends()
    drivers.update(load_extra_backends_fn())
    res = startup_application_fn()
    drivers.update(dependency.resolve_future_dependencies())
    return drivers, res
