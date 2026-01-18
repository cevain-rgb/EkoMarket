from django import forms
from django.forms import modelformset_factory
from .models import Produit, ImageProduit

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fieldStyle = 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
        fields = [
            'titre', 
            'categorie', 
            'etat',
            'prix', 
            'description', 
            'stock',
            'poids',
        ]
        widgets = {
            'titre' : forms.TextInput(attrs = {
                'class' : fieldStyle,
                'placeholder' : 'Ex: iPhone 13 Pro Max - 256Go'
            }),
            'categorie' : forms.Select(attrs = {
                'class' : fieldStyle + ' bg-gray-50',
            }),
            'etat' : forms.Select(attrs = {
                'class' : fieldStyle + ' bg-gray-50',
            }),
            'prix' : forms.TextInput(attrs = {
                'class' : fieldStyle,
                'placeholder' : 'Ex: 850000',
            }),
            'description' : forms.Textarea(attrs = {
                'class' : fieldStyle,
                'rows': 3,
                'placeholder' : 'Décrivez votre produit en détail...'
            }),
            'stock' : forms.TextInput(attrs = {
                'class' : fieldStyle,
                'placeholder' : 'Quantite disponible',
            }),
            'poids' : forms.TextInput(attrs = {
                'class' : fieldStyle,
                'placeholder' : 'Poids',
            }),
            
        }
        

ImageProduitFormSet = modelformset_factory(
    ImageProduit,
    # fields=['image', 'ordre'],
    fields=['image'],
    extra=1,  # Nombre de formulaires vides supplémentaires
    max_num=5,  # Limite à 5 images
    can_delete=True
)