from wsgi_basic.token.persistence.core import Driver


class Token(Driver):

    def create_token(self, token_id, data):
        pass

    def delete_token(self, token_id):
        pass

    def get_token(self, token_id):
        pass

    def clear_expired_tokens(self):
        pass
