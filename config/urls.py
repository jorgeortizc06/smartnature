"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
#from gestion_riego.views import list_persona, new_persona, edit_persona, delete_persona
urlpatterns = [
    path('admin/', admin.site.urls),
    #Vistas basadas en clases, todo lo que hice en view.py, django ya lo hace automaticamente, cambian algunas reglas. class_view.py
    path('gestion_riego/', include("gestion_riego.urls"))
    

    #usado para los view.py.
    #path('list_persona/', list_persona, name='list_persona'),
    #path('new_persona/', new_persona, name='new_persona'),
    #Desde django 2.0 se puede crear urls amigables <int:id>
    #path('editar_persona/<int:id>/', edit_persona, name='edit_persona'),
    #path('delete_persona/<int:id>/', delete_persona, name='delete_persona')


]
