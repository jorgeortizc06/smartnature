"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from dj_static import Cling

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

#application = get_wsgi_application() #funciona solo en local
application = Cling(get_wsgi_application()) #Uso la libreria pip install dj-static que me permite determinar mis archivos estaticos cuando paso a produccion
#tambien se usa pip install gunicorn, esta linea me permite ubicar los archivos estaticos de mi proyecto para que funcione
