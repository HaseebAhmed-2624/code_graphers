from . import environ
import os
from pathlib import Path

# Set the project base directory
BASE_DIR = Path(__file__).resolve().parent.parent



# Take environment variables from .env file
env_dir = os.path.join(BASE_DIR,'envs', '.env')

env = environ.CustomEnvLoader()

if os.path.exists(env_dir):
    environ.CustomEnvLoader.read_env(env_dir)

# from .celery import app as celery_app

# __all__ = ('celery_app',)
