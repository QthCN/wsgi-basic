from wsgi_basic.common import wsgi


latest_app = None


class Version(wsgi.Application):

    def __init__(self, version_type, routers=None):
        self.endpoint_url_type = version_type
        self._routers = routers

        super(Version, self).__init__()

    def _get_versions_list(self, context):
        versions = {}
        versions['v1'] = {
            'id': 'v1',
            'status': 'stable',
            'updated': '2015-09-01T00:00:00Z',
        }

        return versions

    def get_versions(self, context):
        versions = self._get_versions_list(context)
        return wsgi.render_response(body={
            'versions': {
                'values': list(versions.values())
            }
        })
