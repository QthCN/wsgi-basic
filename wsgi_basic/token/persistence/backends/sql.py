from wsgi_basic.token.persistence.core import Driver


class Token(Driver):

    def get_token(self, token_id):
        pass

    def create_token(self, token_id, data):
        pass

    def delete_token(self, token_id):
        pass

    def delete_tokens(self, user_id, tenant_id=None, trust_id=None,
                      consumer_id=None):
        pass

    def _list_tokens(self, user_id, tenant_id=None, trust_id=None,
                     consumer_id=None):
        pass

    def list_revoked_tokens(self):
        pass

    def flush_expired_tokens(self):
        pass