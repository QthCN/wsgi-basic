import logging
import os

from oslo_config import cfg
from oslo_log import log

from wsgi_basic.common import config
from wsgi_basic import exception

CONF = cfg.CONF

configure = config.configure


def setup_logging(project=""):
    log.setup(CONF, project)
    logging.captureWarnings(True)


def set_default_for_default_log_levels():
    extra_log_level_defaults = [
    ]

    log.register_options(CONF)
    CONF.set_default("default_log_levels",
                     CONF.default_log_levels + extra_log_level_defaults)


def find_paste_config():
    if CONF.paste_deploy.config_file:
        paste_config = CONF.paste_deploy.config_file
        paste_config_value = paste_config
        if not os.path.isabs(paste_config):
            paste_config = CONF.find_file(paste_config)
    elif CONF.config_file:
        paste_config = CONF.config_file[0]
        paste_config_value = paste_config

    if not paste_config or not os.path.exists(paste_config):
        raise exception.ConfigFileNotFound(config_file=paste_config_value)
    return paste_config
