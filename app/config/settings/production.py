from .base import *

DEBUG = False

secrets = json.load(open(os.path.join(SECRETS_DIR, 'production.json')))

ALLOWED_HOSTS = []

DATABASES = secrets['DATABASES']
