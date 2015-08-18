from oslo_config import cfg

from wsgi_basic import config


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
