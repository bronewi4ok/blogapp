import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
DEBUG = True

EMAIL_HOST_USER = 'bronewi4ok@gmail.com'
EMAIL_HOST_PASSWORD = 'random@42'
EMAIL_HOST = 'smtp.gmail.com'


# # secure
# CSRF_COOKIE_SECURE = True
# CSRF_COOKIE_SAMESITE = 'Strict'
# SESSION_COOKIE_SECURE = True
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
