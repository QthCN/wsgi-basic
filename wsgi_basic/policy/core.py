# Copyright 2012 OpenStack Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Main entry point into the Policy service."""

import abc

from oslo_config import cfg
import six

from wsgi_basic.common import dependency
from wsgi_basic.common import manager
from wsgi_basic import exception


CONF = cfg.CONF


@dependency.provider('policy_api')
class Manager(manager.Manager):

    driver_namespace = 'wsgi_basic.policy'

    def __init__(self):
        super(Manager, self).__init__(CONF.policy.driver)


@six.add_metaclass(abc.ABCMeta)
class Driver(object):

    @abc.abstractmethod
    def enforce(self, credentials, action, target):
        raise exception.NotImplemented()

