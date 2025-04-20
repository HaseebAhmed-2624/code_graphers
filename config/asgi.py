"""
ASGI config for Nettbox project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

import django
from channels.security.websocket import AllowedHostsOriginValidator

django.setup()
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import apps.websocket.routing
from . import env

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", env.str("DJANGO_SETTINGS_MODULE", "config.settings.local")
)
os.environ.setdefault('USE_PROD_DATABASE', env.str("USE_PROD_DATABASE", False))

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(
            URLRouter(apps.websocket.routing.urlpatterns))
    }
)
