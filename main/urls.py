from django.contrib import admin
from django.urls import path
from .views import index, about, contact_us

urlpatterns = [
    path('', index, name='index'),
    path('/about/', about, name='about'),
    path('/contact/', contact_us, name='contact_us'),
]

