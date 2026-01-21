from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.db.models import Q
from django.contrib import messages
from .models import *
from paniers.models import *

# Create your views here.
# def add_produit_view(request):
#     context = {}
#     return render(request, 'produits/add_produit.html', context)

# ================= catalogue =======================
def catalogue_view(request):
    """
    Vue du catalogue avec filtres et tri
    """
    # produits = Produit.objects.filter(est_actif=True, boutique__statut='ACTIVE')
    produits = Produit.objects.filter(est_actif=True) # a revoir
    
    # Filtres
    categorie = request.GET.get('categorie')
    if categorie:
        produits = produits.filter(categorie__slug=categorie)
    
    recherche = request.GET.get('q')
    if recherche:
        produits = produits.filter(Q(nom__icontains=recherche) | Q(description__icontains=recherche))
    
    prix_min = request.GET.get('prix_min')
    if prix_min:
        produits = produits.filter(prix__gte=prix_min)
    
    prix_max = request.GET.get('prix_max')
    if prix_max:
        produits = produits.filter(prix__lte=prix_max)
    
    # Tri
    tri = request.GET.get('tri', 'nom')
    if tri == 'prix_asc':
        produits = produits.order_by('prix')
    elif tri == 'prix_desc':
        produits = produits.order_by('-prix')
    elif tri == 'nouveau':
        produits = produits.order_by('-created_at')
    else:
        produits = produits.order_by('nom')
    
    # if request.user.is_authenticated:
    # panier = Panier.objects.get(utilisateur=request.user)
    # article_panier = ArticlePanier.objects.filter(panier=panier)
    # else:
        # panier = request.session.get('panier', {}), 
    context = {
        'produits': produits,
        'filtres': {
            'categorie': categorie,
            'recherche': recherche,
            'prix_min': prix_min,
            'prix_max': prix_max,
            'tri': tri,
            # 'panier': article_panier,
        }
    }
    return render(request, 'produits/catalogue.html', context)

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Produit

# ==================== Ajout au panier ====================
@require_POST
def ajouter_au_panier(request):
    """
    Ajouter un produit au panier (session) de l'utilisateur connecté.
    """
    produit_id = request.POST.get('produit_id')
    quantite = int(request.POST.get('quantite', 1))
    
    try:
        produit = Produit.objects.get(id=produit_id, est_actif=True)
        if quantite > produit.stock:
            return JsonResponse({'success': False, 'message': 'Stock insuffisant'})
        
        panier = request.session.get('panier', {})
        if produit_id in panier:
            panier[produit_id]['quantite'] += quantite
        else:
            panier[produit_id] = {
                'nom': produit.nom,
                'prix': str(produit.prix),
                'quantite': quantite,
                'image': produit.image_principale.url if produit.image_principale else None,
            }
            request.session['panier'] = panier
        return JsonResponse({'success': True, 'message': 'Produit ajouté au panier'})
    except Produit.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Produit introuvable'})
    
    # Vue pour Ajouter et editer Produit
    from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProduitForm, ImageProduitFormSet
from .models import Produit

@login_required
def ajouter_produit(request):
    if request.method == 'POST':
        print('heo')
        form = ProduitForm(request.POST)
        formset = ImageProduitFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            produit = form.save(commit=False)
            produit.boutique = request.user.boutique
            produit.save()
            instances = formset.save(commit=False)
            for instance in instances:
                instance.produit = produit
                instance.save()
            messages.success(
                request,
                'Produit publié avec succès!'
            )
            return redirect('catalogue')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
                    
    else:
        form = ProduitForm()
        formset = ImageProduitFormSet()
    return render(request, 'produits/ajouter_produit.html', {'form': form, 'formset': formset})