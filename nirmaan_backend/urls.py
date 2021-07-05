from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls import handler404
from django.conf.urls.static import static
from main.views import password_reset, donations, read_file, donation_cert
from initiatives.views import prd, prd_volunteers, all_visitors, delete_visitor
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='initiatives/login.htm'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='initiatives/logout.htm'), name='logout'),
    path('projects/', include('initiatives.urls')),
    path('', include('main.urls')),
    path('prd/', prd, name='prd'),
    path('prd/volunteers', prd_volunteers, name='prd_volunteers'),
    path('users/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('visitors', all_visitors, name='all_visitors'),
    path('delete_visitor/<int:pk>', delete_visitor, name='delete_visitor'),
    path('donations/', donations, name='donations'),
    path('donations/certificate', donation_cert, name='donation_cert'),
    path('.well-known/pki-validation/404F3EC4D03547B8DFB9F9D284420423.txt', read_file, name='ssl'),
]

handler404 = 'main.views.error_404'
handler500 = 'main.views.error_500'
handler403 = 'main.views.error_403'
handler400 = 'main.views.error_400'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

