import os

from config import ubicacion_archivo

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

POSTGRESQL = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'smartnature',
        'USER': 'jorge',
        'PASSWORD': 'jorge',
        'HOST': ubicacion_archivo.ip_db,
        'DATABASE_PORT': '5432',
    }
}

