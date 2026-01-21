from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Panier, ArticlePanier, Produit
from users.models import Utilisateur

@login_required
def ajouter_au_panier(request, produit_id):
    produit = Produit.objects.get(id=produit_id)
    panier, created = Panier.objects.get_or_create(utilisateur=request.user)
    article_panier, created = ArticlePanier.objects.get_or_create(panier=panier, produit=produit)
    if not created:
        article_panier.quantite += 1
        article_panier.save()
    return redirect('panier')

@login_required
def panier(request):
    panier = Panier.objects.get(utilisateur=request.user)
    articles_panier = ArticlePanier.objects.filter(panier=panier)
    total = sum(article_panier.prix * article_panier.quantite for article_panier in articles_panier)
    return render(request, 'paniers/panier.html', {'panier': panier, 'articles_panier': articles_panier, 'total': total})

@login_required
def supprimer_du_panier(request, article_panier_id):
    article_panier = ArticlePanier.objects.get(id=article_panier_id)
    article_panier.delete()
    return redirect('panier')

@login_required
def vider_panier(request):
    panier = Panier.objects.get(utilisateur=request.user)
    ArticlePanier.objects.filter(panier=panier).delete()
    return redirect('panier')
