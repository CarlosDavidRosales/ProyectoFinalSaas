"""
URL configuration for GestorClinicas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.http import HttpResponseRedirect
from django.conf.urls import handler404

urlpatterns = [
    path('', include('UsersTenants.urls')),
]

# Handler para manejar 404 y redirigir
def custom_page_not_found_view(request, exception):
    if request.get_host() == "http://gestorclinicasdentales.shop":
        return HttpResponseRedirect("http://gestorclinicasdentales.shop")
    else:
        return HttpResponseRedirect("http://gestorclinicasdentales.shop")  # O redirige a la página de inicio de sesión del tenant

handler404 = custom_page_not_found_view