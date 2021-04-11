from django.contrib import admin
from django.urls import path
from .views import index, about, password_reset, internal_index, main_contacts, test_index, troubleshooting, mask_register, mask_sales, masks_dash, mark_order, tnc, privacy_policy, sorad, donation_bill

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
    path('sales', mask_sales, name='sales'),
    path('masks_dash', masks_dash, name='masks_dash'),
    path('<int:pk>/complete', mark_order, name='mark_order'),
    path('terms', tnc, name='tnc'),
    path('policy', privacy_policy, name='ppc'),
    path('sorad', sorad, name='sorad'),
    path('donation_bill', donation_bill, name='donation_bill')
]

