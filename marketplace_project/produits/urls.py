from django.urls import path
from . import views

urlpatterns = [
    # url vers le catalogue (page d'accueil)
    path('', views.catalogue_view, name='catalogue'),
    path('catalogue/', views.catalogue_view, name='catalogue'),
    
    # url vers l'interface dajout d'un produit
    path('ajouter/', views.ajouter_produit, name='ajouter_produit'),
    
    # url panier
    path('ajouter-au-panier/', views.ajouter_au_panier, name='ajouter_au_panier'),
]