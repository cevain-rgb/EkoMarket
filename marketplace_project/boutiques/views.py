from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Boutique
from .forms import *

# Create your views here.

# from .forms import (
# BoutiqueCreationForm, BoutiqueUpdateForm,
# BoutiqueCategoriesForm, ImageBoutiqueForm,
# AvisBoutiqueForm, ReponseAvisForm
# )

def create_boutique_view(request):
    if request.method == 'POST':
        form = BoutiqueCreationForm(request.POST)
        # if form.is_valid():
        try:
            print(f'valid form:{form.is_valid()}')
            shop = form.save()
            shop.save()
            return redirect('boutique_dashboard')
        except Exception as e:
            messages.error(
                request,
                f'Une erreur est survenue lors de la creation de la boutique: {str(e)}'
            )  
    form = BoutiqueCreationForm()           
    return render(request, 'boutiques/create_boutique.html', {'form' : form})
    # return HttpResponse('<h1>creer boutiques</h1>')


# ==================== DÉCORATEURS PERSONNALISÉS ====================
def vendeur_required(view_func):
    """Décorateur pour vérifier que l'utilisateur est un vendeur"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Vous devez être connecté.")
            return redirect('login')
        if not request.user.est_vendeur:
            messages.error(request, "Accès réservé aux vendeurs.")
            # return redirect('user_dashboard')
            return HttpResponse('<h1>Accès réservé aux vendeurs.</h1>')
            
        return view_func(request, *args, **kwargs)
    return wrapper

def boutique_owner_required(view_func):
    """Décorateur pour vérifier que l'utilisateur possède une boutique"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Vous devez être connecté.")
            return redirect('login')
        if not request.user.est_vendeur:
            messages.error(request, "Accès réservé aux vendeurs.")
            # return redirect('user_dashboard')
            return HttpResponse('<h1>Accès réservé aux vendeurs</h1>')
            
        if not hasattr(request.user, 'boutique'):
            messages.warning(request, "Vous devez d'abord crée une boutique.")
            return redirect('create_boutique')
        # else:
        #     messages.warning(request, "Vous avez déjà une boutique.")
        #     return redirect('boutique_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

# ==================== CRÉATION DE BOUTIQUE ====================
@login_required
@vendeur_required
@require_http_methods(["GET", "POST"])
def create_boutique_view(request):
    """
    Vue de création d'une boutique
    """
    # Vérifier si l'utilisateur a déjà une boutique
    if hasattr(request.user, 'boutique'):
        messages.info(request, "Vous avez déjà une boutique.")
        return redirect('boutique_dashboard')
        # return HttpResponse('<h1>Vous avez déjà une boutique.</h1>')
        
    if request.method == 'POST':
        form = BoutiqueCreationForm(request.POST, request.FILES)
        # print(request.POST)
        # print(f'valid form:{form.is_valid()}')

        if form.is_valid():
            try:
                with transaction.atomic():
                    # Créer la boutique
                    boutique = form.save(commit=False)
                    boutique.vendeur = request.user
                    boutique.statut = 'EN_ATTENTE'
                    # En attente de validation
                    boutique.save()
                    # Sauvegarder les catégories (ManyToMany)
                    # form.save_m2m()
                    messages.success(
                    request,
                        'Votre boutique a été créée avec succès ! '
                        'Elle sera validée par notre équipe sous 24-48h.'
                    )
                    return redirect('boutique_dashboard')
                    # return HttpResponse('<h1>boutiques creer</h1>')

            except Exception as e:
                messages.error(
                    request,
                    f'Une erreur est survenue : {str(e)}'
                )
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
                    
    else:
        form = BoutiqueCreationForm()
        
    context = {
        'form': form,
        # 'categories': Categorie.objects.filter(est_active=True)
    }
    return render(request, 'boutiques/create_boutique.html', context)


# ==================== DASHBOARD VENDEUR ====================
@login_required
@boutique_owner_required
def boutique_dashboard_view(request):
    """
    Tableau de bord du vendeur
    """
    boutique = request.user.boutique
    # Statistiques du jour
    today = timezone.now().date()
    
    stats_ventes = {
        'CA' : 0.00, # chiffre d'affaire
    }
    stats_bout = {
        'vues_today' : 0, # Nb de vues de boutiques
        'vues_total' : 0, # Nb de vues de boutiques
        'nouveaux_followers' : 0,
        'followers_total' : 0,
    }
    stats_prod = {
        'actifs' : 0, # Nb de produits actifs
        'vues_today' : 0, # Nb de vues de produits
    }
    stats_com = {
        'com_today' : 0,
        'com_total' : 0,
        'en_attente' : 0,
        'en_cour' : 0,
        'en_effectue' : 0,
    }
    stats_mes = {
        'recus_today' : 0,
        'recus_total' : 0,
        'non_lus' : 0,
    }
    # Statistiques générales
    context = {
        'boutique': boutique,
        'stats' : {
            'ventes': stats_ventes,
            'boutiques': stats_bout,
            'produits': stats_prod,
            'commandes': stats_com,
            'messages': stats_mes,
        }
    }

    return render(request, 'boutiques/boutique_dashboard.html', context)

# ==================== DÉTAIL BOUTIQUE (PUBLIC) ====================
def boutique_detail_view(request, slug):
    """
    Vue publique d'une boutique
    """
    boutique = get_object_or_404(Boutique, slug=slug)
    
    # Vérifier si la boutique est active
    if boutique.statut != 'ACTIVE' and (not request.user.is_authenticated or request.user != boutique.vendeur):
        messages.error(request, "Cette boutique n'est pas disponible.")
        # return HttpResponse('<h1>Cette boutique n\'est pas disponible.</h1>')
    
    # Incrémenter les vues (stats)
    # today = timezone.now().date()
    # stats, created = StatistiqueBoutique.objects.get_or_create(
    #     boutique=boutique,
    #     date=today
    # )
    # stats.vues_boutique += 1
    # stats.save()
    
    # Récupérer les produits (à compléter avec le modèle Produit)
    # produits = boutique.produits.filter(est_actif=True)[:12]
    
    # Récupérer les avis
    # avis = boutique.avis.filter(est_publie=True).order_by('-created_at')[:10]
    # # Vérifier si l'utilisateur suit la boutique
    # is_following = False
    # if request.user.is_authenticated and request.user.is_acheteur:
    #     is_following = SuiviBoutique.objects.filter(
    #         client=request.user,
    #         boutique=boutique
    #     ).exists()
    context = {
        'boutique': boutique,
        # 'produits': produits,
        # 'avis': avis,
        # 'is_following': is_following,
    }
    return render(request, 'boutiques/boutique_detail.html', context)


# ==================== PARAMÈTRES BOUTIQUE ====================
@login_required
@boutique_owner_required
@require_http_methods(["GET", "POST"])
def boutique_settings_view(request):
    """
    Paramètres de la boutique
    """
    boutique = request.user.boutique
    if request.method == 'POST':
        form = BoutiqueUpdateForm(request.POST, request.FILES, instance=boutique)
        # form = BoutiqueCreationForm(request.POST, request.FILES, instance=boutique)
        if form.is_valid():
            form.save()
            messages.success(request, "Boutique mise à jour avec succès !")
            return redirect('boutique_settings')
        else:
            messages.error(request, "Veuillez corriger les erreurs.")
    else:
        form = BoutiqueUpdateForm(instance=boutique)
        # form = BoutiqueCreationForm(instance=boutique)
        context = {
            'form': form,
            'boutique': boutique,
        }
    return render(request, 'boutiques/boutique_settings.html', context)
    # return render(request, 'boutiques/create_boutique.html', context)
    
# ==================== GESTION DES CATÉGORIES ====================
@login_required
@boutique_owner_required
@require_http_methods(["GET", "POST"])
def boutique_categories_view(request):
    """
    Gérer les catégories de la boutique
    """
    boutique = request.user.boutique

    if request.method == 'POST':
        form = BoutiqueCategoriesForm(request.POST, instance=boutique)
    
        if form.is_valid():
            form.save()
            messages.success(request, "Catégories mises à jour !")
            return redirect('boutique_settings')
        else:
            messages.error(request, "Veuillez corriger les erreurs.")
    else:
        form = BoutiqueCategoriesForm(instance=boutique)

    context = {
        'form': form,
        'boutique': boutique,
    }
    return render(request, 'boutiques/boutique_categories.html', context)

# ==================== LISTE DES BOUTIQUES ====================
def boutiques_list_view(request):
    """
    Liste de toutes les boutiques actives
    """
    # Filtres
    categorie_slug = request.GET.get('categorie')
    ville = request.GET.get('ville')
    search = request.GET.get('search')
    sort = request.GET.get('sort', '-created_at')
    # Query de base
    # boutiques = Boutique.objects.filter(statut='ACTIVE')
    # a modifier
    boutiques = Boutique.objects.all()
    # Appliquer les filtres
    if categorie_slug:
        boutiques = boutiques.filter(categories__slug=categorie_slug)
    if ville:
        boutiques = boutiques.filter(ville__iexact=ville)
    if search:
        boutiques = boutiques.filter(
            Q(nom__icontains=search) |
            Q(description__icontains=search) |
            Q(secteur_activite__icontains=search)
        )
    # Tri
    sort_options = {
        'recent': '-created_at',
        'nom': 'nom',
        'note': '-note_moyenne',
        'ventes': '-nombre_ventes',
    }
    boutiques = boutiques.order_by(sort_options.get(sort, '-created_at'))# Pagination
    paginator = Paginator(boutiques, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Villes disponibles (pour le filtre)
    villes = Boutique.objects.filter(
        statut='ACTIVE'
    ).values_list('ville', flat=True).distinct()
    
    context = {
        'page_obj': page_obj,
        'categories': Categorie.objects.filter(est_active=True, parent__isnull=True),   
        'villes': villes,
        'current_categorie': categorie_slug,
        'current_ville': ville,
        'current_search': search,
        'current_sort': sort,
    }
    
    return render(request, 'boutiques/boutique_list.html', context)