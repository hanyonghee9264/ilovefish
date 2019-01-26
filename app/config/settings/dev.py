from .base import *

DEBUG = True

secrets = json.load(open(os.path.join(SECRETS_DIR, 'dev.json')))

ALLOWED_HOSTS = []

DATABASES = secrets['DATABASES']
