from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register_view, name = 'register'),
    path('login/', views.login_view, name = 'login'),
    path('profil/<int:id>/', views.profil_view, name = 'profil'),
    path('logout/', views.logout_view, name = 'logout'),
] 