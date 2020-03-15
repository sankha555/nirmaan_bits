from django.contrib import admin
from django.urls import path
from .views import index, index2, about, contact_us

urlpatterns = [
    path('', index, name='index'),
    path('/contact', index2, name='index2'),
    path('/about/', about, name='about'),
    path('/contact/', contact_us, name='contact_us'),
]

