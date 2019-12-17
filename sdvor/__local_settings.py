import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sdvor',
        'USER': 'postgres',
        'PASSWORD': 'Kjdh23098uijlkahs09d-2h3byutf',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


ALLOWED_HOSTS = ['159.69.16.1']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/sdvor.log',
            'maxBytes': 1024 * 1024 * 15,  # 5 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'ERROR',
            'propagate': True
        },
    }
}
