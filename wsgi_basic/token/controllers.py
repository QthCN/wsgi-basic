from wsgi_basic import exception
from wsgi_basic.common import controller
from wsgi_basic.common import dependency


@dependency.requires("token_api", "token_provider_api")
class Auth(controller.V1Controller):

    def authenticate(self, context, auth=None):
        username = auth.get("username", None)
        password = auth.get("password", None)
        if username is None or password is None:
            raise exception.Unauthorized()

        if self.token_api.validate_user(username, password):
            token = self.token_provider_api.gen_token_id(auth)
            self.token_api.create_token(token, dict(username=username))
            return dict(token=token)
        raise exception.Unauthorized()

    @controller.protected()
    def delete_token(self, context, token_id):
        self.token_api.delete_token(token_id)

    @controller.protected()
    def validate_token(self, context, token_id):
        return self.token_api.get_token(token_id)
