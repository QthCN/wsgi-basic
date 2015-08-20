from wsgi_basic import token
from wsgi_basic import policy


def load_backends():

    DRIVERS = dict(
        token_provider_api=token.providers.Manager(),
        token_api=token.persistence.Manager(),
        policy_api=policy.Manager(),
    )

    return DRIVERS
