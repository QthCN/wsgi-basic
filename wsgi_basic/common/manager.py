import functools

from oslo_log import log
from oslo_log import versionutils
from oslo_utils import importutils
import stevedore


LOG = log.getLogger(__name__)


def load_driver(namespace, driver_name, *args):
    try:
        driver_manager = stevedore.DriverManager(namespace,
                                                 driver_name,
                                                 invoke_on_load=True,
                                                 invoke_args=args)
        return driver_manager.driver
    except RuntimeError as e:
        LOG.debug('Failed to load %r using stevedore: %s', driver_name, e)
        # Ignore failure and continue on.

    def _load_using_import(driver_name, *args):
        return importutils.import_object(driver_name, *args)

    # For backwards-compatibility, an unregistered class reference can
    # still be used.
    return _load_using_import(driver_name, *args)


class Manager(object):
    """Base class for intermediary request layer.

    The Manager layer exists to support additional logic that applies to all
    or some of the methods exposed by a service that are not specific to the
    HTTP interface.

    It also provides a stable entry point to dynamic backends.

    An example of a probable use case is logging all the calls.

    """

    driver_namespace = None

    def __init__(self, driver_name):
        self.driver = load_driver(self.driver_namespace, driver_name)

    def __getattr__(self, name):
        """Forward calls to the underlying driver."""
        f = getattr(self.driver, name)
        setattr(self, name, f)
        return f
