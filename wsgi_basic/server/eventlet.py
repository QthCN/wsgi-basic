import os

from oslo_concurrency import processutils
from oslo_config import cfg


CONF = cfg.CONF


def _get_workers(worker_type_config_opt):
    # Get the value from config, if the config value is None (not set), return
    # the number of cpus with a minimum of 2.
    worker_count = CONF.eventlet_server.get(worker_type_config_opt)
    if not worker_count:
        worker_count = max(2, processutils.get_worker_count())
    return worker_count


def run(possible_topdir, conf_dir="etc", conf_file="wsgi_basic.conf"):
    dev_conf = os.path.join(possible_topdir,
                            conf_dir,
                            conf_file)
    config_files = None
    if os.path.exists(dev_conf):
        config_files = [dev_conf]
