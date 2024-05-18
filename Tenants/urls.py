from django.contrib import admin
from django.urls import path
from .views import register, home

urlpatterns = [
    path('', home, name='Home'),
    path('admin/', admin.site.urls),
    path('register/', register, name='register')
]
