from django.urls import path
from . import views
    
urlpatterns = [
    path('ajouter-au-panier/<int:produit_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('panier/', views.panier, name='panier'),
    path('supprimer-du-panier/<int:article_panier_id>/', views.supprimer_du_panier, name='supprimer_du_panier'),
    path('vider-panier/', views.vider_panier, name='vider_panier'),
]