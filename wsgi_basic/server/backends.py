from wsgi_basic import token
from wsgi_basic import policy
from wsgi_basic import user


def load_backends():

    DRIVERS = dict(
        token_provider_api=token.providers.Manager(),
        token_api=token.persistence.Manager(),
        policy_api=policy.Manager(),
        user_api=user.Manager(),
    )

    return DRIVERS
