from wsgi_basic.common import controller
from wsgi_basic.common import dependency


@dependency.requires("token_api")
class Auth(controller.V1Controller):

    def authenticate(self, context, auth=None):
        print("in authenticate")
        print context
        print auth
        print self.token_api.get_token(1)
        return "token111222333444555"
