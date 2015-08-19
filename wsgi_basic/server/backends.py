from wsgi_basic import token


def load_backends():

    DRIVERS = dict(
        token_provider_api=token.providers.Manager(),
        token_api=token.persistence.Manager(),
    )

    return DRIVERS
