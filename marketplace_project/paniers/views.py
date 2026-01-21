from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Panier, ArticlePanier, Produit
from users.models import Utilisateur
from django.http import JsonResponse

@login_required
def ajouter_au_panier(request):
    """
    Ajouter un produit au panier de l'utilisateur connecté.
    """
    produit_id = request.POST.get('produit_id')
    quantite = int(request.POST.get('quantite', 1))

    try:
        # produit = Produit.objects.get(id=produit_id, est_actif=True)
        produit = Produit.objects.get(id=produit_id)
        if quantite > produit.stock:
            return JsonResponse({'success': False, 'message': 'Stock insuffisant'})
        
        produit = Produit.objects.get(id=produit_id)
        panier, created = Panier.objects.get_or_create(utilisateur=request.user)
        article_panier, created = ArticlePanier.objects.get_or_create(panier=panier, produit=produit)
        if not created:
            article_panier.quantite += 1
            article_panier.save()
        return JsonResponse({'success': True, 'message': 'Produit ajouté au panier'})
    except Produit.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Produit introuvable'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    # return redirect('panier')

@login_required
def panier(request):
    panier = Panier.objects.get(utilisateur=request.user)
    articles_panier = ArticlePanier.objects.filter(panier=panier)
    total = sum(article_panier.produit.prix * int(article_panier.quantite) for article_panier in articles_panier)
    context = {
        'panier': panier, 
        'articles_panier': articles_panier, 
        'total': total
    }
    return render(request, 'paniers/panier.html', context)

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
    
@login_required
def modifier_quantite_panier(request, article_panier_id):
    """
    Modifier la quantité d'un produit dans le panier.
    """
    try:
        article_panier = ArticlePanier.objects.get(id=article_panier_id)
        nouvelle_quantite = int(request.POST.get('quantite', 1))
        
        if nouvelle_quantite <= 0:
            article_panier.delete()
        elif nouvelle_quantite > article_panier.produit.stock:
            return JsonResponse({'success': False, 'message': 'Stock insuffisant'})
        else:
            article_panier.quantite = nouvelle_quantite
            article_panier.save()
        
        return JsonResponse({'success': True, 'message': 'Quantité mise à jour'})
    except ArticlePanier.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Article introuvable'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

