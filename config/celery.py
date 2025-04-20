import os
from pathlib import Path

from . import environ
from celery import Celery

# Set the project base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file
env_dir = os.path.join(BASE_DIR, 'envs', '.env')

env = environ.CustomEnvLoader()

if os.path.exists(env_dir):
    environ.CustomEnvLoader.read_env(env_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', env.str("DJANGO_SETTINGS_MODULE", 'config.settings.local'))
os.environ.setdefault('USE_PROD_DATABASE', env.str("USE_PROD_DATABASE", "False"))

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


