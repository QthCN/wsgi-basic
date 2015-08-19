from wsgi_basic.common import wsgi
from wsgi_basic import controllers

class Versions(wsgi.ComposableRouter):

    def __init__(self, description):
        self.description = description

    def add_routes(self, mapper):
        version_controller = controllers.Version(self.description)
        mapper.connect("/",
                       controller=version_controller,
                       action="get_versions")
