"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from . import env
os.environ.setdefault('DJANGO_SETTINGS_MODULE',  env.str("DJANGO_SETTINGS_MODULE",'config.settings.local') )
os.environ.setdefault('USE_PROD_DATABASE',  env.bool("USE_PROD_DATABASE",False) )

application = get_wsgi_application()


