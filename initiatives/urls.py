from django.contrib import admin
from django.urls import path
from .views import (home, create_initiative, update_initiative, 
                     InitiativeDeleteView, init_detail,
                     like_initiative, volunteers)
from django.contrib.admin.views.decorators import staff_member_required

urlpatterns = [
    path('', home, name='home'),
    path('create', create_initiative, name='init_create' ),
    path('<str:slug>/update', update_initiative, name='init_update' ),
    path('<str:slug>/delete', InitiativeDeleteView.as_view(), name='init_delete' ),
    path('<str:slug>', init_detail, name='init_detail' ),
    path('<str:slug>/volunteers', volunteers, name='volunteers' ),
    path('<int:pk>/liked', like_initiative, name='like_initiative' ),
    path('update_projects', update_projects, name='update_projects'),
]

