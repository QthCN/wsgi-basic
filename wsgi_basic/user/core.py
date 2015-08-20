from wsgi_basic.common import dependency


@dependency.provider("user_api")
class Manager(object):

    def create_user(self, username, password, role):
        pass

    def delete_user(self, user_id):
        pass

    def update_user(self, user_id, password):
        pass

    def get_user(self, user_id):
        pass

    def get_users(self):
        pass
