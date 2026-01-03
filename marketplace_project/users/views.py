from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from . import forms
import uuid
#  INSCRPTION
@require_http_methods(['GET', 'POST'])
def register_view(request):
    """ vue dinscription des utilisateurs """
    if request.user.is_authenticated:
        return redirect(f"/users/profil/{request.user.id}/")
    
    if request.method == 'POST':
        form = forms.UserRegisterForm(request.POST)
        if form.is_valid():
            try:
                #  creation de l'user
                user = form.save()
                # user.set_is_active(True)
                # user.username = f"user_{uuid.uuid4().hex[:8]}"
                user.save()
                # connexion de lutilisateur apres incription
                login(request, user)
                return redirect(f"/users/profil/{request.user.id}/")
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
        form = forms.UserRegisterForm()           
    return render(request, 'users/inscription.html', {'form' : form})

# CONNEXION ET DECONNEXION
@require_http_methods(['GET', 'POST'])
def login_view(request):
    """  Vue de connxion """
    if request.user.is_authenticated:
        return redirect(f"/users/profil/{request.user.id}/")
    
    if request.method == 'POST':
        form = forms.UserLoginForm(request.POST)
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
            
            # redirection vers la page de profil
            return redirect(f"/users/profil/{request.user.id}/")
            
        else:
            messages.error(request, 'Email ou mot de passe incorrect.')
            # Log echec de connexion
            try:
                user = Utilisateur.objects.get(email=email)
                log_login_attemp(user, request, success=False, reason='Mot de passe incorrect')
            except Utilisateur.DoesNotExist:
                pass
        # else:
        #     messages.error(request, 'Veuillez corriger les erreurs ce-dessous.')
            
    else:
        form = forms.UserLoginForm
        
    return render(request, 'users/connexion.html', {'form' : form})


@login_required
def logout_view(request):
    """ Vue de deconnxion """
    logout(request)
    messages.success(request, 'Vous avez ete deconnecte avec succes.')
    
    return redirect('/users/login')

@login_required
def profil_view(request, id):
    """ Page de profit  """
    return render(request, 'users/profil.html', {'data' : f"profil utilisateur:{id}"})