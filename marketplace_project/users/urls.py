from django.contrib import admin
from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

# urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = [
    # inscription, connexion et deconnxion d'utilisateur
    path('register/', views.register_view, name = 'register'),
    path('login/', views.login_view, name = 'login'),
    path('', views.login_view, name = 'login'),
    path('logout/', views.logout_view, name = 'logout'),
    
    # profil utilisateur
    # path('profil/<int:id>/', views.profil_view, name = 'profil'),
    path('profile/', views.profile_view, name = 'profile'),
]
