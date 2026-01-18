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
    
    
    
class UserProfileUpdateForm(forms.ModelForm):
    """
    Formulaire de mise à jour du profil utilisateur
    """
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Prénom'
        }),
        label="Prénom"
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom'
        }),
        label="Nom"
    )
    
    telephone = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+237XXXXXXXXX'
        }),
        label="Téléphone"
    )
    
    adresse = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3
        }),
        label="Adresse"
    )
    
    ville = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        label="Ville"
    )
    
    class Meta:
        model = Utilisateur
        fields = ['first_name', 'last_name', 'telephone', 'adresse', 'ville']
    
    def clean_telephone(self):
        """Valide le format du téléphone"""
        phone = self.cleaned_data.get('telephone')
        phone = re.sub(r'[^\d+]', '', phone)
        
        if not re.match(r'^\+?237?[0-9]{9}$', phone):
            raise ValidationError("Format de téléphone invalide.")
        
        if not phone.startswith('+'):
            if phone.startswith('237'):
                phone = '+' + phone
            else:
                phone = '+237' + phone
        
        return phone
    
class UserProfileUpdateForm(forms.ModelForm):
    """
    Formulaire de mise à jour du profil utilisateur
    """
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Prénom'
        }),
        label="Prénom"
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom'
        }),
        label="Nom"
    )
    
    telephone = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+237XXXXXXXXX'
        }),
        label="Téléphone"
    )
    
    adresse = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3
        }),
        label="Adresse"
    )
    
    ville = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        label="Ville"
    )
    
    class Meta:
        model = Utilisateur
        fields = ['first_name', 'last_name', 'telephone', 'adresse', 'ville']
    
    def clean_telephone(self):
        """Valide le format du téléphone"""
        phone = self.cleaned_data.get('telephone')
        phone = re.sub(r'[^\d+]', '', phone)
        
        if not re.match(r'^\+?237?[0-9]{9}$', phone):
            raise ValidationError("Format de téléphone invalide.")
        
        if not phone.startswith('+'):
            if phone.startswith('237'):
                phone = '+' + phone
            else:
                phone = '+237' + phone
        
        return phone


class UserProfileExtendedForm(forms.ModelForm):
    """
    Formulaire pour les informations étendues du profil
    (bio, préférences, etc.)
    """
    class Meta:
        model = Utilisateur
        fields = ['avatar', 'bio', 'preferred_language', 
                'email_notifications', 'sms_notifications']
        widgets = {
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Parlez-nous un peu de vous...',
                'maxlength': '500'
            }),
            'preferred_language': forms.Select(attrs={
                'class': 'form-select'
            }),
            'email_notifications': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'sms_notifications': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'avatar': 'Photo de profil',
            'bio': 'Biographie',
            'preferred_language': 'Langue préférée',
            'email_notifications': 'Recevoir les notifications par email',
            'sms_notifications': 'Recevoir les notifications par SMS'
        }
    
    def clean_avatar(self):
        """Valide la taille et le type de l'image"""
        avatar = self.cleaned_data.get('avatar')
        
        if avatar:
            # Vérifier la taille (max 2MB)
            if avatar.size > 2 * 1024 * 1024:
                raise ValidationError("L'image ne doit pas dépasser 2 MB.")
            
            # Vérifier le type de fichier
            valid_types = ['image/jpeg', 'image/png', 'image/jpg', 'image/webp']
            if avatar.content_type not in valid_types:
                raise ValidationError(
                    "Format d'image non supporté. Utilisez JPEG, PNG ou WebP."
                )
        
        return avatar


"""
Prénom * 
Nom * 
Email * 
Téléphone 
Mot de passe * 
Confirmer le mot de passe * 
Type de compte
"""