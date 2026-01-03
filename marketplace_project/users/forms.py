from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, ValidationError
import re

Utilisateur = get_user_model()

class UserRegisterForm(UserCreationForm):
    fieldStyle = 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'

    class Meta:
        model = Utilisateur
        fieldStyle = 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
        fields = ['first_name', 'last_name', 'username', 'email', 'telephone', 'type_utilisateur', 'password1', 'password2']
        widgets = {
            'first_name' : forms.TextInput(attrs = {
                'class' : fieldStyle,
                'placeholder' : 'Prénom'
            }),
            'last_name' : forms.TextInput(attrs = {
                'class' : fieldStyle,
                'placeholder' : 'Nom'
            }),
            'username' : forms.TextInput(attrs = {
                'class' : fieldStyle,
                'placeholder' : 'Nom utilisateur'
            }),
            'email' : forms.TextInput(attrs = {
                'class' : fieldStyle,
                'placeholder' : 'Votre@email.com'
            }),
            'telephone' : forms.TextInput(attrs = {
                'class' : fieldStyle,
                'placeholder' : '+237 XXX XXX XXX OU 6XX XXX XXX'
            }),
            'type_utilisateur' : forms.Select(attrs = {
                'class' : fieldStyle + ' bg-gray-50',
            }),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personnalisation des champs de mot de passe
        self.fields['password1'].widget.attrs.update({ 'class': self.fieldStyle, 'placeholder': 'Mot de passe' })
        self.fields['password2'].widget.attrs.update({ 'class': self.fieldStyle, 'placeholder': 'Confirmer le mot de passe' })

    def clean_email(self):
        """ verifie qusie l'email n'existe pas deja"""
        email = self.cleaned_data.get('email')
        if Utilisateur.objects.filter(email=email).exists():
            raise ValidationError('Cette adresse email est deja utilise')
        return email.lower()
    
    def clean_username(self):
        """ verifie que le username n'existe pas deja"""
        username = self.cleaned_data.get('username')
        if Utilisateur.objects.filter(username=username).exists():
            raise ValidationError('Ce nom d\'utilisateur est deja utilise')
        return username.lower()
    
    def clean_telephone(self):
        """ permet de valider et formater le numero de telephone"""
        phone = self.cleaned_data.get('telephone')
        # Enlevement des espaces et caracteres speciaux
        phone = re.sub(r'[^\d+]', '', phone)
        
        # Normalisation au format international
        if not phone.startswith('+'):
            if phone.startswith('237'):
                phone = '+' + phone
            else:
                phone = '+237' + phone
        return phone
    
    # def clean_password2(self):
    #     """ Validation personnalisee du mot de passe """
    #     password1 = self.cleaned_data.get('password1')
    #     password2 = self.cleaned_data.get('password2')
        
    #     if password1 and password2 and password1 != password2:
    #         raise ValidationError('Les mots de passes ne correspondent pas.')
        
    #     #  verification de la force dumot de passe
    #     if len(password1) < 8:
    #         raise ValidationError('Le mots de passe doit contenir au moins 8 caracteres')
        
    #     if not re.search(r'[A-Z]', password1):
    #         raise ValidationError('Le mots de passe doit contenir au moins une majuscule')
        
    #     if not re.search(r'[a-z]', password1):
    #         raise ValidationError('Le mots de passe doit contenir au moins une minicule')
        
    #     if not re.search(r'[0-9]', password1):
    #         raise ValidationError('Le mots de passe doit contenir au moins un chiffre')
    #     return password2
                
                

class UserLoginForm(AuthenticationForm):
    fieldStyle = 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
    
    username = forms.CharField(label = 'Email', 
        widget = forms.TextInput(attrs = {
            'class' : fieldStyle,
            'placeholder' : 'Votre@email.com',
        }),
    )
    password = forms.CharField(max_length = 50,label = 'Mot de passe', 
        widget = forms.PasswordInput(attrs = {
            'class' : fieldStyle,
            'placeholder' : 'Mot de passe',
        }),
    )
    
    remember_me = forms.BooleanField(
        required = False,
        label = 'Se souvenir de moi',
        widget = forms.CheckboxInput(attrs = {
            'class' : 'h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'
        })
    )

"""
Prénom * 
Nom * 
Email * 
Téléphone 
Mot de passe * 
Confirmer le mot de passe * 
Type de compte
"""