from __future__ import absolute_import

import uuid

from wsgi_basic.token.providers.core import Driver


class Provider(Driver):

    def gen_token_id(self, token_data):
        return uuid.uuid4().hex

