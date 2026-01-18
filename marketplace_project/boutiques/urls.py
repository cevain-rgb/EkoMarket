from django.urls import path
from . import views

urlpatterns = [
    # ==================== CRÉATION & GESTION BOUTIQUE ====================
    # Créer une boutique
    path('create/', views.create_boutique_view, name='create_boutique'),
    
    # Dashboard vendeur
    path('dashboard/', views.boutique_dashboard_view, name='boutique_dashboard'),
    
    # Paramètres de la boutique
    path('settings/', views.boutique_settings_view, name='boutique_settings'),
    
    # Gestion des catégories
    path('categories/', views.boutique_categories_view, name='boutique_categories'),
    
    # ==================== PAGES PUBLIQUES ====================
    # Liste de toutes les boutiques
    path('', views.boutiques_list_view, name='boutiques_list'),

    # Détail d'une boutique (EN DERNIER pour éviter les conflits)
    path('<slug:slug>/', views.boutique_detail_view, name='boutique_detail'),
]