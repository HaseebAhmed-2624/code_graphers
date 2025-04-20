import secrets


def identifier():
    return secrets.token_urlsafe(32)