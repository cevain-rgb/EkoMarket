from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from boutiques.models import Boutique, Categorie
import uuid

class Produit(models.Model):
    ETAT_CHOIX = [
        ('NEUF', 'Neuf'),
        ('BON', 'Bon'),
        ('USE', 'Use'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    boutique = models.ForeignKey(Boutique, on_delete=models.CASCADE, related_name='produits')
    nom = models.CharField(max_length=200, null=True, blank=True, verbose_name="Titre du produit")
    titre = models.CharField(max_length=200, null=False, verbose_name="Titre du produit")
    slug = models.SlugField(unique=True, blank=True)
    etat = models.CharField(max_length=10,  choices=ETAT_CHOIX,  default='Neuf', verbose_name="État du produit")
    description = models.TextField(verbose_name="Description")
    prix = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name='Prix (FCFA)')
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, related_name='produits', verbose_name='Catégorie')
    image_principale = models.ImageField(upload_to='produits/', blank=True, null=True)
    est_actif = models.BooleanField(default=True)
    stock = models.IntegerField(default=0, null=False, validators=[MinValueValidator(0)], verbose_name='Quantite disponible')
    poids = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Poids')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ['-created_at']
        
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.images.count() > 5:
            raise ValidationError("Un produit ne peut avoir que 5 images maximum.")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.slug:
            self.slug = slugify(f'{self.titre}{self.id}')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titre

    def est_en_stock(self):
        return self.stock > 0

# models pour les images associer a un produit
class ImageProduit(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='produits/images/')
    ordre = models.PositiveIntegerField(default=0, help_text="Ordre d'affichage")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Image du produit"
        verbose_name_plural = "Images du produit"
        ordering = ['ordre']

    def __str__(self):
        return f"Image de {self.produit.titre}"