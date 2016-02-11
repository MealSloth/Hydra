from databases import databases

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Michael', 'michael@mealsloth.com'),
)

MANAGERS = ADMINS

DATABASES = databases()

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'blob.mealsloth.com']

TIME_ZONE = 'America/Chicago'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = True

SECRET_KEY = '%v0-hkr&oobscc7*!wrc=!e3@d85q9ede0(nzljkoz@)j5+l(&'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
)

ROOT_URLCONF = 'Hydra.urls'

WSGI_APPLICATION = 'Hydra.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'lib.cloudstorage',
    'Hydra',
)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Google Cloud Storage

GCS_CLIENT_ID = 'mealsloth-dryad-bu01'

GOOGLE_CLOUD_STORAGE_BUCKET = '/' + GCS_CLIENT_ID
GOOGLE_CLOUD_STORAGE_URL = 'http://storage.googleapis.com/'
GOOGLE_CLOUD_STORAGE_DEFAULT_CACHE_CONTROL = 'public, max-age: 7200'

DEFAULT_FILE_STORAGE = 'google.storage.google_cloud.GoogleCloudStorage'
