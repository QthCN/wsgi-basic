import logging
import os
import socket

from oslo_concurrency import processutils
from oslo_config import cfg
from oslo_service import service
from oslo_service import systemd
import pbr.version

from wsgi_basic import config
from wsgi_basic.common import environment
from wsgi_basic.server import common
from wsgi_basic import service as wsgi_basic_service


CONF = cfg.CONF


class ServerWrapper(object):
    """Wraps a Server with some launching info & capabilities."""

    def __init__(self, server, workers):
        self.server = server
        self.workers = workers

    def launch_with(self, launcher):
        self.server.listen()
        if self.workers > 1:
            # Use multi-process launcher
            launcher.launch_service(self.server, self.workers)
        else:
            # Use single process launcher
            launcher.launch_service(self.server)


def serve(*servers):
    if max([server[1].workers for server in servers]) > 1:
        launcher = service.ProcessLauncher(CONF)
    else:
        launcher = service.ServiceLauncher(CONF)

    for name, server in servers:
        try:
            server.launch_with(launcher)
        except socket.error:
            logging.exception("Failed to start the %(name)s server" % {
                "name": name})
            raise

    # notify calling process we are ready to serve
    systemd.notify_once()

    for name, server in servers:
        launcher.wait()


def _get_workers(worker_type_config_opt):
    # Get the value from config, if the config value is None (not set), return
    # the number of cpus with a minimum of 2.
    worker_count = CONF.eventlet_server.get(worker_type_config_opt)
    if not worker_count:
        worker_count = max(2, processutils.get_worker_count())
    return worker_count


def configure_threading():
    monkeypatch_thread = not CONF.standard_threads
    environment.use_eventlet(monkeypatch_thread)


def create_server(conf, name, host, port, workers):
    app = wsgi_basic_service.loadapp('config:%s' % conf, name)
    server = environment.Server(app, host=host, port=port,
                                keepalive=CONF.eventlet_server.tcp_keepalive,
                                keepidle=CONF.eventlet_server.tcp_keepidle)
    if CONF.eventlet_server_ssl.enable:
        server.set_ssl(CONF.eventlet_server_ssl.certfile,
                       CONF.eventlet_server_ssl.keyfile,
                       CONF.eventlet_server_ssl.ca_certs,
                       CONF.eventlet_server_ssl.cert_required)
    return name, ServerWrapper(server, workers)


def run(possible_topdir, conf_dir="etc", conf_file="wsgi-basic.conf"):
    dev_conf = os.path.join(possible_topdir,
                            conf_dir,
                            conf_file)
    config_files = None
    if os.path.exists(dev_conf):
        config_files = [dev_conf]

    common.configure(
        version=pbr.version.VersionInfo("wsgi_basic").version_string(),
        config_files=config_files,
        pre_setup_logging_fn=configure_threading)

    paste_config = config.find_paste_config()

    def create_servers():
        public_worker_count = _get_workers("public_workers")

        servers = []
        servers.append(create_server(paste_config,
                                     "main",
                                     CONF.eventlet_server.public_bind_host,
                                     CONF.eventlet_server.public_port,
                                     public_worker_count))

        return servers

    _unused, servers = common.setup_backends(
        startup_application_fn=create_servers
    )

    serve(*servers)
