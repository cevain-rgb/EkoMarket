from django import forms
from django.core.exceptions import ValidationError
from .models import *
import re

class BoutiqueCreationForm(forms.ModelForm):
    """
    Formulaire de création d'une boutique
    """
    categories = forms.ModelMultipleChoiceField(
        queryset=Categorie.objects.filter(est_active=True, parent__isnull=False),
        
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        required=False,
        label="Catégories de produits"
    )
    accepte_conditions = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label="J'accepte les conditions générales de vente"
    )
    
    class Meta:
        model = Boutique
        fields = [
            'nom', 'description', 'secteur_activite', 'categories',
            'adresse', 'ville', 'telephone', 'email',
            'logo', 'site_web', 'facebook', 'instagram'
        ]        
        # fields = [
        #     'nom', 'description', 'secteur_activite',
        #     'adresse', 'ville', 'telephone', 'email',
        #     'logo', 'site_web', 'facebook', 'instagram'
        # ]
        fieldStyle = 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': fieldStyle,
                'placeholder': 'Nom de votre boutique'
            }),
            'description': forms.Textarea(attrs={
                'class': fieldStyle,
                'placeholder': 'Décrivez votre boutique et vos produits...',
                'rows': 5
            }),
            'secteur_activite': forms.TextInput(attrs={
                'class': fieldStyle,
                'placeholder': 'Ex: Électronique, Mode, Alimentation...'
            }),
            'adresse': forms.Textarea(attrs={
                'class': fieldStyle,
                'placeholder': 'Adresse complète de votre boutique',
                'rows': 3
            }),
            'ville': forms.TextInput(attrs={
                'class': fieldStyle,
                'placeholder': 'Ville'
            }),
            'telephone': forms.TextInput(attrs={
                'class': fieldStyle,
                'placeholder': '+237 6XX XXX XXX'
            }),
            'email': forms.EmailInput(attrs={
                'class': fieldStyle,
                'placeholder': 'contact@votreboutique.com'
            }),
            'logo': forms.FileInput(attrs={
                'class': fieldStyle,
                'accept': 'image/*'
            }),
            'site_web': forms.URLInput(attrs={
                'class': fieldStyle,
                'placeholder': 'https://www.votresite.com'
            }),
            'facebook': forms.URLInput(attrs={
                'class': fieldStyle,
                'placeholder': 'https://facebook.com/votreboutique'
            }),
            'instagram': forms.URLInput(attrs={
                'class': fieldStyle,
                'placeholder': 'https://instagram.com/votreboutique'
            }),
        }
        labels = {
            'nom': 'Nom de la boutique',
            'description': 'Description',
            'secteur_activite': 'Secteur d\'activité',
            'categorie': "Catégories de produits",
            'adresse': 'Adresse',
            'ville': 'Ville',
            'telephone': 'Téléphone',
            'email': 'Email de contact',
            'logo': 'Logo (optionnel)',
            'site_web': 'Site web (optionnel)',
            'facebook': 'Facebook (optionnel)',
        }
        
    def clean_nom(self):
        """Valider le nom de la boutique"""
        nom = self.cleaned_data.get('nom')
        # Vérifier si le nom existe déjà
        if Boutique.objects.filter(nom__iexact=nom).exists():
            raise ValidationError("Ce nom de boutique est déjà utilisé.")
        # Vérifier la longueur minimale
        if len(nom) < 3:
            raise ValidationError("Le nom doit contenir au moins 3 caractères.")
        return nom
    def clean_telephone(self):
        """Valider le numéro de téléphone"""
        telephone = self.cleaned_data.get('telephone')
        phone = re.sub(r'[^\d+]', '', telephone)
        if not re.match(r'^\+?237?[0-9]{9}$', phone):
            raise ValidationError("Format invalide. Utilisez: +237XXXXXXXXX ou 6XXXXXXXX")
        # Normaliser au format international
        if not phone.startswith('+'):
            if phone.startswith('237'):
                phone = '+' + phone
            else:
                phone = '+237' + phone
        return phone
    
    def clean_logo(self):
        """Valider le logo"""
        logo = self.cleaned_data.get('logo')
        if logo:
            # Vérifier la taille (max 2MB)
            if logo.size > 2 * 1024 * 1024:
                raise ValidationError("Le logo ne doit pas dépasser 2 MB.")
            
        # Vérifier le type
        valid_types = ['image/jpeg', 'image/png', 'image/jpg', 'image/webp']
        # if logo.content_type not in valid_types:
        #     raise ValidationError("Format non supporté. Utilisez JPEG, PNG ou WebP.")
        return logo
    
class BoutiqueUpdateForm(forms.ModelForm):
    """
    Formulaire de mise à jour d'une boutique
    """
    class Meta:
        model = Boutique
        fields = [
            'nom', 'description', 'secteur_activite',
            'adresse', 'ville', 'telephone', 'email',
            'logo', 'banniere', 'site_web', 
            'facebook', 'instagram', 'twitter'
        ]
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'rows': 5
            }),
            'secteur_activite': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
            }),
            'adresse': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'rows': 3
            }),
            'ville': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
            }),
            'logo': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'accept': 'image/*'
            }),
            'banniere': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'accept': 'image/*'
            }),
            'site_web': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
            }),
            'facebook': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
            }),
            'instagram': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
            }),
            'twitter': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
            }),
        }
    
    def clean_categories(self):
        """Valider les catégories"""
        categories = self.cleaned_data.get('categories')
        if not categories:
            raise ValidationError("Sélectionnez au moins une catégorie.")
        if categories.count() > 5:
            raise ValidationError("Vous ne pouvez sélectionner que 5 catégories maximum.")
        return categories
    
class BoutiqueCategoriesForm(forms.ModelForm):
    """
    Formulaire pour gérer les catégories de la boutique
    """
    categories = forms.ModelMultipleChoiceField(
        queryset=Categorie.objects.filter(est_active=True, parent__isnull=False),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        required=True,
        label="Catégories de produits"
    )
    class Meta:
        model = Boutique
        fields = ['categories']
