from oslo_config import cfg
from oslo_log import log
from oslo_utils import encodeutils


CONF = cfg.CONF
LOG = log.getLogger(__name__)


class Error(Exception):
    """Base error class.

    Child classes should define an HTTP status code, title, and a
    message_format.

    """
    code = None
    title = None
    message_format = None

    def __init__(self, message=None, **kwargs):
        try:
            message = self._build_message(message, **kwargs)
        except KeyError:
            LOG.warning('missing exception kwargs (programmer error)')
            message = self.message_format

        super(Error, self).__init__(message)

    def _build_message(self, message, **kwargs):
        """Builds and returns an exception message.

        :raises: KeyError given insufficient kwargs

        """
        if not message:
            try:
                message = self.message_format % kwargs
            except UnicodeDecodeError:
                try:
                    kwargs = {k: encodeutils.safe_decode(v)
                              for k, v in kwargs.items()}
                except UnicodeDecodeError:
                    message = self.message_format
                else:
                    message = self.message_format % kwargs

        return message


class SecurityError(Error):
    """Avoids exposing details of security failures, unless in debug mode."""
    amendment = "(Disable debug mode to suppress these details.)"

    def _build_message(self, message, **kwargs):
        """Only returns detailed messages in debug mode."""
        if CONF.debug:
            return "%(message)s %(amendment)s" % {
                'message': message or self.message_format % kwargs,
                'amendment': self.amendment}
        else:
            return self.message_format % kwargs


class UnexpectedError(SecurityError):
    """Avoids exposing details of failures, unless in debug mode."""
    _message_format = ("An unexpected error prevented the server "
                       "from fulfilling your request.")

    debug_message_format = ("An unexpected error prevented the server "
                            "from fulfilling your request: %(exception)s")

    @property
    def message_format(self):
        """Return the generic message format string unless debug is enabled."""
        if CONF.debug:
            return self.debug_message_format
        return self._message_format

    def _build_message(self, message, **kwargs):
        if CONF.debug and "exception" not in kwargs:
            # Ensure that exception has a value to be extra defensive for
            # substitutions and make sure the exception doesn't raise an
            # exception.
            kwargs["exception"] = ""
        return super(UnexpectedError, self)._build_message(message, **kwargs)

    code = 500
    title = "Internal Server Error"


class ConfigFileNotFound(UnexpectedError):
    debug_message_format = ("The Keystone configuration file %(config_file)s "
                            "could not be found.")


class Unauthorized(SecurityError):
    message_format = "The request you have made requires authentication."
    code = 401
    title = 'Unauthorized'


class AuthPluginException(Unauthorized):
    message_format = "Authentication plugin error."

    def __init__(self, *args, **kwargs):
        super(AuthPluginException, self).__init__(*args, **kwargs)
        self.authentication = {}


class ValidationError(Error):
    message_format = ("Expecting to find %(attribute)s in %(target)s -"
                       " the server could not comply with the request"
                       " since it is either malformed or otherwise"
                       " incorrect. The client is assumed to be in error.")
    code = 400
    title = 'Bad Request'

class NotFound(Error):
    message_format = "Could not find: %(target)s"
    code = 404
    title = 'Not Found'
