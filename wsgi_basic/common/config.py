from oslo_config import cfg


CONF = cfg.CONF


# add file options here
FILE_OPTIONS = {
    None: [
        cfg.StrOpt('admin_token', secret=True, default='ADMIN',
                   help='A "shared secret" that can be used to bootstrap '
                        'Keystone. This "token" does not represent a user, '
                        'and carries no explicit authorization. To disable '
                        'in production (highly recommended), remove '
                        'AdminTokenAuthMiddleware from your paste '
                        'application pipelines (for example, in '
                        'keystone-paste.ini).'),
        cfg.IntOpt('max_param_size', default=64,
                   help='Limit the sizes of user & project ID/names.'),
        # we allow tokens to be a bit larger to accommodate PKI
        cfg.IntOpt('max_token_size', default=8192,
                   help='Similar to max_param_size, but provides an '
                        'exception for token values.'),
        # NOTE(lbragstad/morganfainberg): This value of 10k was
        # measured as having an approximate 30% clock-time savings
        # over the old default of 40k.  The passlib default is not
        # static and grows over time to constantly approximate ~300ms
        # of CPU time to hash; this was considered too high.  This
        # value still exceeds the glibc default of 5k.
        cfg.IntOpt('crypt_strength', default=10000,
                   help='The value passed as the keyword "rounds" to '
                        'passlib\'s encrypt method.'),
        cfg.IntOpt('list_limit',
                   help='The maximum number of entities that will be '
                        'returned in a collection, with no limit set by '
                        'default. This global limit may be then overridden '
                        'for a specific driver, by specifying a list_limit '
                        'in the appropriate section (e.g. [assignment]).'),
        cfg.BoolOpt('strict_password_check', default=False,
                    help='If set to true, strict password length checking is '
                         'performed for password manipulation. If a password '
                         'exceeds the maximum length, the operation will fail '
                         'with an HTTP 403 Forbidden error. If set to false, '
                         'passwords are automatically truncated to the '
                         'maximum length.'),
        cfg.StrOpt('secure_proxy_ssl_header',
                   help='The HTTP header used to determine the scheme for the '
                        'original request, even if it was removed by an SSL '
                        'terminating proxy. Typical value is '
                        '"HTTP_X_FORWARDED_PROTO".'),
    ],
    'paste_deploy': [
        cfg.StrOpt('config_file', default='wsgi-basic-paste.ini',
                   help='Name of the paste configuration file that defines '
                        'the available pipelines.'),
    ],
    'eventlet_server': [
        cfg.IntOpt('public_workers',
                   deprecated_name='public_workers',
                   deprecated_group='DEFAULT',
                   deprecated_for_removal=True,
                   help='The number of worker processes to serve the public '
                        'eventlet application. Defaults to number of CPUs '
                        '(minimum of 2).'),
        cfg.StrOpt('public_bind_host',
                   default='0.0.0.0',
                   deprecated_opts=[cfg.DeprecatedOpt('bind_host',
                                                      group='DEFAULT'),
                                    cfg.DeprecatedOpt('public_bind_host',
                                                      group='DEFAULT'), ],
                   deprecated_for_removal=True,
                   help='The IP address of the network interface for the '
                        'public service to listen on.'),
        cfg.IntOpt('public_port', default=5000, deprecated_name='public_port',
                   deprecated_group='DEFAULT',
                   deprecated_for_removal=True,
                   help='The port number which the public service listens '
                        'on.'),
        cfg.BoolOpt('wsgi_keep_alive', default=True,
                    help="If set to false, disables keepalives on the server; "
                         "all connections will be closed after serving one "
                         "request."),
        cfg.IntOpt('client_socket_timeout', default=900,
                   help="Timeout for socket operations on a client "
                        "connection. If an incoming connection is idle for "
                        "this number of seconds it will be closed. A value "
                        "of '0' means wait forever."),
        cfg.BoolOpt('tcp_keepalive', default=False,
                    deprecated_name='tcp_keepalive',
                    deprecated_group='DEFAULT',
                    deprecated_for_removal=True,
                    help='Set this to true if you want to enable '
                         'TCP_KEEPALIVE on server sockets, i.e. sockets used '
                         'by the wsgi-basic wsgi server for client '
                         'connections.'),
        cfg.IntOpt('tcp_keepidle',
                   default=600,
                   deprecated_name='tcp_keepidle',
                   deprecated_group='DEFAULT',
                   deprecated_for_removal=True,
                   help='Sets the value of TCP_KEEPIDLE in seconds for each '
                        'server socket. Only applies if tcp_keepalive is '
                        'true.'),
    ],
    'eventlet_server_ssl': [
        cfg.BoolOpt('enable', default=False, deprecated_name='enable',
                    deprecated_group='ssl',
                    deprecated_for_removal=True,
                    help='Toggle for SSL support on the wsgi-basic '
                         'eventlet servers.'),
        cfg.StrOpt('certfile',
                   default="/etc/wsgi-basic/ssl/certs/wsgi-basic.pem",
                   deprecated_name='certfile', deprecated_group='ssl',
                   deprecated_for_removal=True,
                   help='Path of the certfile for SSL. For non-production '
                        'environments, you may be interested in using '
                        '`wsgi-basic-manage ssl_setup` to generate self-signed '
                        'certificates.'),
        cfg.StrOpt('keyfile',
                   default='/etc/wsig-basic/ssl/private/wsgi-basic.pem',
                   deprecated_name='keyfile', deprecated_group='ssl',
                   deprecated_for_removal=True,
                   help='Path of the keyfile for SSL.'),
        cfg.StrOpt('ca_certs',
                   default='/etc/wsgi-basic/ssl/certs/ca.pem',
                   deprecated_name='ca_certs', deprecated_group='ssl',
                   deprecated_for_removal=True,
                   help='Path of the CA cert file for SSL.'),
        cfg.BoolOpt('cert_required', default=False,
                    deprecated_name='cert_required', deprecated_group='ssl',
                    deprecated_for_removal=True,
                    help='Require client certificate.'),
    ],
    'token': [
        cfg.IntOpt('expiration', default=3600,
                   help='Amount of time a token should remain valid '
                        '(in minutes).'),
        cfg.StrOpt('provider',
                   default='uuid',
                   help='Controls the token construction, validation, and '
                        'revocation operations. Entrypoint in the '
                        'keystone.token.provider namespace. Core providers '
                        'are [fernet|pkiz|pki|uuid].'),
        cfg.StrOpt('driver',
                   default='sql',
                   help='Entrypoint for the token persistence backend driver '
                        'in the keystone.token.persistence namespace.'),
    ],
    'policy': [
        cfg.StrOpt('driver',
                   default='sql',
                   help='Entrypoint for the policy backend driver in the '
                        'wsgi_basic.policy namespace.'),
    ],
    'mysql': [
        cfg.StrOpt('host',
                   default='127.0.0.1',
                   help='MySQL DB host address.'),
        cfg.IntOpt('port',
                   default=3306,
                   help='MySQL DB port.'),
        cfg.StrOpt('username',
                   default='root',
                   help='MySQL DB user.'),
        cfg.StrOpt('password',
                   default='rootroot',
                   help='MySQL DB password.'),
        cfg.StrOpt('schema',
                   default='wsgi_basic',
                   help='MySQL DB default schema'),
    ],
}


def configure(conf=None):
    if conf is None:
        conf = CONF

    conf.register_cli_opt(
        cfg.BoolOpt('standard-threads', default=False,
                    help='Do not monkey-patch threading system modules.'))

    for section in FILE_OPTIONS:
        for option in FILE_OPTIONS[section]:
            if section:
                conf.register_opt(option, group=section)
            else:
                conf.register_opt(option)


def list_opts():
    """Return a list of oslo_config options available.

    The returned list includes all oslo_config options which are registered as
    the "FILE_OPTIONS" in wsgi_basic.common.config. This list will not include
    the options from the oslo-incubator library or any options registered
    dynamically at run time.

    Each object in the list is a two element tuple. The first element of
    each tuple is the name of the group under which the list of options in the
    second element will be registered. A group name of None corresponds to the
    [DEFAULT] group in config files.

    This function is also discoverable via the 'oslo_config.opts' entry point
    under the 'wsgi_basic.config.opts' namespace.

    The purpose of this is to allow tools like the Oslo sample config file
    generator to discover the options exposed to users by this library.

    :returns: a list of (group_name, opts) tuples
    """
    return list(FILE_OPTIONS.items())

