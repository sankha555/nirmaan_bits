from django.contrib import admin
from django.urls import path
from .views import index, contact, about, password_reset, internal_index

urlpatterns = [
    path('', index, name='index'),
    path('contact', contact, name='contact_us'),
    path('about', about, name='about'),
    path('reset_password', password_reset, name='pwd_reset'),
    path(' ', internal_index, name='internal_index'),
]

