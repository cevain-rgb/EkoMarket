from django.db import models
from users.models import Utilisateur
from django.utils.text import slugify
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Categorie(models.Model):
    """
    Modèle pour les catégories de produits
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100, unique=True, verbose_name="Nom")
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name="Description")
    
    # Icône pour la catégorie (FontAwesome class ou image)
    icone = models.CharField(max_length=50, blank=True, default="fa-tag")
    
    # Hiérarchie (catégorie parente)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='sous_categories',
        verbose_name="Catégorie parente"
    )
    
    # Ordre d'affichage
    ordre = models.IntegerField(default=0, verbose_name="Ordre")
    
    # Statut
    est_active = models.BooleanField(default=True, verbose_name="Active")
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['ordre', 'nom']
        
    def __str__(self):
        return self.nom
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
            super().save(*args, **kwargs)
            
    def get_produits_count(self):
        """Retourne le nombre de produits dans cette catégorie"""
        from .models import Produit
        return Produit.objects.filter(categorie=self, est_actif=True).count()


class Boutique(models.Model):
    """
    Modele pour la boutique du vendeur
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vendeur = models.OneToOneField(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='boutique',
        limit_choices_to={'type_utilisateur': 'VENDEUR'}
    )

    # Informations de base
    nom = models.CharField(max_length=200, unique=True, blank=True, null=True, verbose_name="Nom de la boutique")
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField(verbose_name="Description")
    
    # Logo et bannière
    logo = models.ImageField(
        upload_to='boutiques/logos/',
        blank=True,
        null=True,
        verbose_name="Logo"
    )
    banniere = models.ImageField(
        upload_to='boutiques/bannieres/',
        blank=True,
        null=True,
        verbose_name="Bannière"
    )
    
    # Secteur d'activité
    secteur_activite = models.CharField(
        max_length=100,
        verbose_name="Secteur d'activité"
    )
    
    # Catégories de produits vendus
    categories = models.ManyToManyField(
        Categorie,
        related_name='boutiques',
        verbose_name="Catégories de produits"
    )
    
    # Coordonnées
    adresse = models.TextField(verbose_name="Adresse")
    ville = models.CharField(max_length=100, verbose_name="Ville")
    telephone = models.CharField(max_length=15, verbose_name="Téléphone")
    email = models.EmailField(verbose_name="Email de contact")
    
    # Réseaux sociaux
    site_web = models.URLField(blank=True, verbose_name="Site web")
    facebook = models.URLField(blank=True, verbose_name="Facebook")
    instagram = models.URLField(blank=True, verbose_name="Instagram")
    twitter = models.URLField(blank=True, verbose_name="Twitter")       

    # Statut
    STATUT_CHOICES = [
        ('EN_ATTENTE', 'En attente de validation'),
        ('ACTIVE', 'Active'),
        ('SUSPENDUE', 'Suspendue'),
        ('FERMEE', 'Fermée'),
    ]
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='EN_ATTENTE',
        verbose_name="Statut"
    )
    
    # Options premium
    est_premium = models.BooleanField(default=False, verbose_name="Compte premium")
    premium_expire_le = models.DateTimeField(null=True, blank=True)
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")
    validee_le = models.DateTimeField(null=True, blank=True, verbose_name="Date de validation")
    
    validee_par = models.ForeignKey(Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='boutiques_validees',
        verbose_name="Validée par"
    )
    
    class Meta:
        verbose_name = "Boutique"
        verbose_name_plural = "Boutiques"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
            super().save(*args, **kwargs)
    @property
    def est_active(self):
        """Vérifie si la boutique est active"""
        return self.statut == 'ACTIVE'
    @property
    def peut_vendre(self):
        """Vérifie si la boutique peut vendre"""
        return self.statut == 'ACTIVE' and self.vendeur.is_active
    def get_produits_actifs(self):
        """Retourne les produits actifs de la boutique"""
        return self.produits.filter(est_actif=True)
    def get_url(self):
        """Retourne l'URL de la boutique"""
        return f"/boutiques/{self.slug}/"
    

class AvisBoutique(models.Model):
    """
    Modèle pour les avis sur les boutiques
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    boutique = models.ForeignKey(
        Boutique,
        on_delete=models.CASCADE,
        related_name='avis',
        verbose_name="Boutique"
    )
    client = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='avis_boutiques',
        limit_choices_to={'user_type': 'ACHETEUR'}
    )
    # Note et commentaire
    note = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Note"
    )
    titre = models.CharField(max_length=200, verbose_name="Titre")
    commentaire = models.TextField(verbose_name="Commentaire")# Critères spécifiques
    note_produits = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Note produits"
    )
    note_service = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Note service"
    )
    note_livraison = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Note livraison"
    )
    # Statut
    est_publie = models.BooleanField(default=True, verbose_name="Publié")
    est_verifie = models.BooleanField(default=False, verbose_name="Achat vérifié")
    
    # Réponse du vendeur
    reponse = models.TextField(blank=True, verbose_name="Réponse du vendeur")
    repondu_le = models.DateTimeField(null=True, blank=True)
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Avis boutique"
        verbose_name_plural = "Avis boutiques"
        ordering = ['-created_at']
        unique_together = ['boutique', 'client'] # Un seul avis par client
    def __str__(self):
        return f"Avis de {self.client.get_full_name()} sur {self.boutique.nom}"
    # def save(self, *args, **kwargs):
        # super().save(*args, **kwargs)
        # Mettre à jour la note moyenne de la boutique
        # self.boutique.calculer_note_moyenne()
        
    class SuiviBoutique(models.Model):
        """
        Modèle pour suivre une boutique (favoris)
        """
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        client = models.ForeignKey(
            Utilisateur,
            on_delete=models.CASCADE,
            related_name='boutiques_suivies',
            limit_choices_to={'user_type': 'ACHETEUR'}
        )
        boutique = models.ForeignKey(
            Boutique,
            on_delete=models.CASCADE,
            related_name='followers'
        )
        # Options de notification
        notifications_nouveaux_produits = models.BooleanField(
            default=True,
            verbose_name="Notifications nouveaux produits"
        )
        
        notifications_promotions = models.BooleanField(
            default=True,
            verbose_name="Notifications promotions"
        )
        
        created_at = models.DateTimeField(auto_now_add=True)
        
        class Meta:
            verbose_name = "Suivi de boutique"
            verbose_name_plural = "Suivis de boutiques"
            ordering = ['-created_at']
            unique_together = ['client', 'boutique']
        def __str__(self):
            return f"{self.client.get_full_name()} suit {self.boutique.nom}"
        
    class StatistiqueBoutique(models.Model):
        """
        Modèle pour les statistiques journalières des boutiques
        """
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        boutique = models.ForeignKey(
            Boutique,
            on_delete=models.CASCADE,
            related_name='statistiques'
        )
        date = models.DateField(verbose_name="Date")
        # Vues
        vues_boutique = models.IntegerField(default=0, verbose_name="Vues boutique")
        vues_produits = models.IntegerField(default=0, verbose_name="Vues produits")
        # Ventes
        nombre_commandes = models.IntegerField(default=0, verbose_name="Nombre de commandes")
        chiffre_affaires = models.DecimalField(
            max_digits=10,
            decimal_places=2,
            default=0.00,
            verbose_name="Chiffre d'affaires"
        )# Engagement
        nouveaux_followers = models.IntegerField(default=0, verbose_name="Nouveaux followers")
        messages_recus = models.IntegerField(default=0, verbose_name="Messages reçus")
        created_at = models.DateTimeField(auto_now_add=True)
        class Meta:
            verbose_name = "Statistique boutique"
            verbose_name_plural = "Statistiques boutiques"
            ordering = ['-date']
            unique_together = ['boutique', 'date']
        def __str__(self):
            return f"Stats {self.boutique.nom} - {self.date}"