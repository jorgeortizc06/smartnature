import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

POSTGRESQL = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'smartnature',
        'USER': 'jorge',
        'PASSWORD': 'jorge',
        'HOST': '192.168.100.254',
        'DATABASE_PORT': '5432',
    }
}

