from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from . import forms
from .forms import *
from .models import *
import uuid

#  INSCRPTION
@require_http_methods(['GET', 'POST'])
def register_view(request):
    """ Vue d'inscription des utilisateurs """
    if request.user.is_authenticated:
        return redirect(f"/users/profile")
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            try:
                #  creation de l'user
                user = form.save()
                # user.set_is_active(True)
                # user.username = f"user_{uuid.uuid4().hex[:8]}"
                user.save()
                # connexion de lutilisateur apres incription
                login(request, user)
                return redirect(f"/users/profile")
            except Exception as e:
                messages.error(
                    request,
                    f'Une erreur est survenue lors de l\'inscription: {str(e)}'
                )   
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserRegisterForm()           
    return render(request, 'users/inscription.html', {'form' : form})

# CONNEXION ET DECONNEXION
@require_http_methods(['GET', 'POST'])
def login_view(request):
    """  Vue de connxion """
    if request.user.is_authenticated:
        return redirect(f"/users/profile")
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        print(request.POST)
        # if form.is_valid():
        email = request.POST['username']
        password = request.POST['password']
        # remember_me = request.POST['remember_me']
        # Authentification
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)

            # Gestion de se souvenir de moi
            # if not remember_me:
            #     request.session.set_expiry(0) #expiration de la session des la fermeture du site
            # else:
            #     request.session.set_expiry(1209600) #Apres 2 semaines
            
            # Log de connexion
            # log_login_attemp(user, request, success=True)
            
            messages.success(request, f'Bienvenue {user.get_full_name()} !')
            
            # redirection vers la page de profile
            return redirect(f"/users/profile")
            
        else:
            messages.error(request, 'Email ou mot de passe incorrect.')
            # Log echec de connexion
            # try:
            #     user = Utilisateur.objects.get(email=email)
            #     log_login_attemp(user, request, success=False, reason='Mot de passe incorrect')
            # except Utilisateur.DoesNotExist:
            #     pass
        # else:
        #     messages.error(request, 'Veuillez corriger les erreurs ce-dessous.')
            
    else:
        form = UserLoginForm()
        
    return render(request, 'users/connexion.html', {'form' : form})


@login_required
def logout_view(request):
    """ Vue de deconnxion """
    logout(request)
    messages.success(request, 'Vous avez ete deconnecte avec succes.')
    
    return redirect('/users/login')

@login_required
@require_http_methods(["GET", "POST"])
def profile_view(request):
    """Vue et édition du profil utilisateur"""
    user = request.user
    
    
    if request.method == 'POST':
        user_form = UserProfileUpdateForm(request.POST, instance=user)
        profile_form = UserProfileExtendedForm(
            request.POST, 
            request.FILES, 
            instance=user
        )
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profil mis à jour avec succès !')
            return redirect('profile')
        else:
            messages.error(request, 'Veuillez corriger les erreurs.')
    else:
        user_form = UserProfileUpdateForm(instance=user)
        profile_form = UserProfileExtendedForm(instance=user)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'users/profile.html', context)


def boutique_detail(request, slug):
    """
    Vue publique de la boutique
    Accessible à tous les visiteurs
    """
    boutique = get_object_or_404(Boutique, slug=slug)
    
    # Vérifier que la boutique est active
    if boutique.statut != 'ACTIVE' and (
        not request.user.is_authenticated or 
        request.user != boutique.vendeur
    ):
        messages.error(request, "Cette boutique n'est pas disponible.")
        # return redirect('home')
        # return HttpResponse("Boutique inactive.", status=403)
        pass
    
    # Statistiques de vue (uniquement pour les visiteurs, pas le propriétaire)
    if not request.user.is_authenticated or request.user != boutique.vendeur:
        today = timezone.now().date()
        stats, created = StatistiqueBoutique.objects.get_or_create(
            boutique=boutique,
            date=today
        )
        stats.vues_boutique += 1
        stats.save()
    
    # Produits de la boutique (à compléter avec le modèle Produit)
    # produits = boutique.produits.filter(est_actif=True)[:12]
    
    # Avis de la boutique
    avis = boutique.avis.filter(est_publie=True).order_by('-created_at')[:5]
    
    # Vérifier si l'utilisateur suit la boutique
    est_suivi = False
    if request.user.is_authenticated and request.user.est_acheteur:
        est_suivi = SuiviBoutique.objects.filter(
            client=request.user,
            boutique=boutique
        ).exists()
    
    context = {
        'boutique': boutique,
        # 'produits': produits,
        'avis': avis,
        'est_suivi': est_suivi,
    }
    
    return render(request, 'boutiques/boutique_detail.html', context)
