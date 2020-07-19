from django.contrib import admin
from django.urls import path
from .views import (volunteer_login_validation, pl_dashboard, register_visitor, profile, update_volunteers)
from django.contrib.admin.views.decorators import staff_member_required

urlpatterns = [
    path('', volunteer_login_validation, name='validation'),
    path('profile', profile, name='profile'),
    path('pl_dashboard', pl_dashboard, name='pl_dashboard'),
    path('visitor', register_visitor, name='register_visitor'),
    path('update_volunteers', update_volunteers, name='update_volunteers')
]