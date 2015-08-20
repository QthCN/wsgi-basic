from wsgi_basic.common import wsgi
from wsgi_basic.user import controllers


class Router(wsgi.ComposableRouter):

    def add_routes(self, mapper):
        user_controller = controllers.User()
        mapper.connect('/users',
                       controller=user_controller,
                       action='create_user',
                       conditions=dict(method=['POST']))
        mapper.connect('/users/{user_id}',
                       controller=user_controller,
                       action='get_user',
                       conditions=dict(method=['GET']))
        mapper.connect('/users/{user_id}',
                       controller=user_controller,
                       action='delete_user',
                       conditions=dict(method=['DELETE']))
        mapper.connect('/users/{user_id}',
                       controller=user_controller,
                       action='update_user',
                       conditions=dict(method=['PUT']))
        mapper.connect('/users',
                       controller=user_controller,
                       action='get_users',
                       conditions=dict(method=['GET']))
