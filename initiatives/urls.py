from django.contrib import admin
from django.urls import path
from .views import (home, create_initiative, update_initiative, 
                     InitiativeDeleteView, init_detail,
                     like_initiative, dash)
from django.contrib.admin.views.decorators import staff_member_required

urlpatterns = [
    path('', home, name='home'),
    path('create', create_initiative, name='init_create' ),
    path('<int:pk>/update', update_initiative, name='init_update' ),
    path('<int:pk>/delete', staff_member_required(InitiativeDeleteView.as_view()), name='init_delete' ),
    path('<int:pk>', init_detail, name='init_detail' ),
    path('<int:pk>/liked', like_initiative, name='like_initiative' ),
    #path('post/<int:pk>/comment/', add_comment, name='add_comment'),
    
]

