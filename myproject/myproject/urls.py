
from django.contrib import admin
from django.urls import path

from myapp import views

urlpatterns = [
    path('auth/', views.auth_form, name='auth_form'),
    path('auth/get_user_key/', views.get_user_key, name='get_user_key'),
    path('auth/unified_auth/', views.unified_auth, name='unified_auth'),
    path('profile_page/', views.profile_page, name='profile_page'),
    path('add_inviter/', views.add_inviter, name='add_inviter'),
]