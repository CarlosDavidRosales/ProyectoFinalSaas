# UserTenants/urls.py

from django.urls import path
from .views import index, user_profile, inventory_list, staff_list, logout_view

urlpatterns = [
    path('', index, name='index'),
    path('Profile/' , user_profile, name='Profile')
]
