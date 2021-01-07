from django.contrib import admin
from django.urls import path
from .views import index, about, password_reset, internal_index, main_contacts, test_index, troubleshooting, mask_register, mask_sales

urlpatterns = [
    path('index', internal_index, name='internal_index'),
    path('', index, name='index'),
    #path('contact', contact, name='contact_us'),
    path('about', about, name='about'),
    path('leads', main_contacts, name='main_contacts'),
    path('reset_password', password_reset, name='pwd_reset'),
    #path('test', test_index, name='test_index'),
    path('site_help', troubleshooting, name='troubleshooting'),
    path('peahen', mask_register, name='mask_register'),
    path('sales', mask_sales, name='mask_sales'),

]

