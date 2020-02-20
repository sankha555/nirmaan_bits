from django.contrib import admin
from django.urls import path
from .views import (home, create_initiative, update_initiative, 
                     InitiativeDeleteView, InitiativeDetailView, add_comment,
                     like_initiative)

urlpatterns = [
    path('', home, name='home'),
    path('initiatives/create', create_initiative, name='init_create' ),
    path('initiatives/<int:pk>/update', update_initiative, name='init_update' ),
    path('initiatives/<int:pk>/delete', InitiativeDeleteView.as_view(), name='init_delete' ),
    path('initiatives/<int:pk>', InitiativeDetailView.as_view(), name='init_detail' ),
    path('initiatives/<int:pk>/liked', like_initiative, name='like_initiative' ),
    path('post/<int:pk>/comment/', add_comment, name='add_comment'),
]

