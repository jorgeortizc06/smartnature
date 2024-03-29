"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from config import db

BASE_DIR = Path(__file__).resolve().parent.parent

print("Tu base es:", BASE_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'n1_r6$u5#xurw8j+5$yx#hra-(4k*gyqyu)97(4)dn9iqp56yg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']  # alojas tu ip servidor

# Application definition

INSTALLED_APPS = [
    # 'gestion_riego.apps.GestionRiegoConfig',
    'gestion_riego',
    'rest_framework',
    'corsheaders',
    'django.contrib.admin',  # Para el panel de control django
    'django.contrib.auth',
    'django.contrib.contenttypes',  # tipo de contenido utilizado
    'django.contrib.sessions',  # Sessiones
    'django.contrib.messages',  # Mensajes de error
    'django.contrib.staticfiles',  # Para los archivos css
    'django_extensions',  # para jupyter notebook python manage.py shell_plus --notebook
    'sslserver',
]

CORS_ALLOW_ALL_ORIGINS = True

MIDDLEWARE = [  # intermediarios, seguridad. Usuario y framework. Seguridad por defecto. ex: inyecciones sql
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

# Jupiter Notebook Settings
NOTEBOOK_ARGUMENTS = [
    '--ip', '0.0.0.0',
    '--allow-root',
    '--no-browser',
]

ROOT_URLCONF = 'config.urls'  # Hace referencia a las rutas principales del proyecto

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'  # enlaza a wsgi.py: para parte de produccion

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
# Configuracion de la base de datos. Por defecto utiliza sqlite3. Puede trabajar con un o varias DB
DATABASES = db.POSTGRESQL

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators
# Proteccion de las contraseñas comunes
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Configuracion de ssl, por ahora esta en True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
}

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'es-ec'

# Django por general siempre recupera o setea la hora en formato UTC
TIME_ZONE = 'America/Guayaquil'

USE_I18N = True

USE_L10N = True

USE_TZ = False  # Me daba problemas con la zona horaria, con esto desabilito la zona horario de django

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

LOGIN_URL = '/gestion-riego/login'
LOGIN_REDIRECT_URL = '/gestion-riego/dashboard'
LOGOUT_REDIRECT_URL = '/gestion-riego/login'

# Se utilizo para poder utilizar ORM en jupyter notebook desactivar la async
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

# Para el guardado de las imagenes de logica difusa
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'gestion_riego/media/')
