from .base import *

SECRET_KEY = 'django-insecure-5q-txbrm9-9g*!ebz^m9!pscvby3g1+y!5_@5tjrdz3lul(@&('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# STATIC_URL = 'static/'
#
# STATICFILES_DIRS = [
#      BASE_DIR / "static"
# ]
#
# STATIC_ROOT = BASE_DIR / 'staticfiles'

# Defined my - Static URL
STATIC_URL = 'static/'

STATICFILES_DIRS = [
    #BASE_DIR / "static"
    os.path.join(BASE_DIR, 'static')
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = 'media/'

MEDIA_ROOT = BASE_DIR / 'media'

