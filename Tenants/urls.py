# urls.py
from django.contrib import admin
from django.urls import path, include
from .views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Asegúrate de que el nombre de la vista sea 'home'
    path('', include('UsersTenants.urls')),  # Incluir URLs de la aplicación UsersTenants
]
