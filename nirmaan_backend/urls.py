"""nirmaan_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from main.views import password_reset
from initiatives.views import prd, prd_volunteers, all_visitors, delete_visitor

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
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
