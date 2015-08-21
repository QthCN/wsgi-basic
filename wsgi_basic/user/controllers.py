from wsgi_basic import exception
from wsgi_basic.common import controller
from wsgi_basic.common import dependency

@dependency.requires("user_api")
class User(controller.V1Controller):

    @controller.protected()
    def create_user(self, context, username=None, password=None, role=None):
        if role is None or role not in ("admin", "user"):
            raise exception.RoleNotFound()
        return self.user_api.create_user(username, password, role)

    @controller.protected()
    def delete_user(self, context, user_id):
        self.user_api.delete_user(user_id)

    @controller.protected()
    def update_user(self, context, user_id, password):
        self.user_api.get_user(user_id)
        return self.user_api.update_user(user_id, password)

    @controller.protected()
    def get_user(self, context, user_id):
        return self.user_api.get_user(user_id)

    @controller.protected()
    def get_users(self, context):
        return self.user_api.get_users()
