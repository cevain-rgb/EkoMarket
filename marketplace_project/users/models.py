from django.db import models

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
# import uuid

class Utilisateur(AbstractUser):
    """
    Modèle utilisateur personnalisé pour EkoMarket
    Gère les acheteurs, vendeurs et administrateurs
    """
    USER_TYPE_CHOICES = [
        ('ACHETEUR', 'Acheteur'),
        ('VENDEUR', 'Vendeur'),
        ('ADMIN', 'Administrateur'),
    ]
    # identifiant
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255,default=None, unique=True, verbose_name="Username")
    # username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    
    type_utilisateur = models.CharField(
        max_length=10, 
        choices=USER_TYPE_CHOICES, 
        default='ACHETEUR',
        verbose_name="Type d'utilisateur"
    )
    
    # Informations personnelles
    regex_telephone = RegexValidator(
        regex=r'^\+?237?[0-9]{9}$',
        message="Le numéro doit être au format: '+237XXXXXXXXX' ou '6XXXXXXXX'"
    )
    telephone = models.CharField(
        validators=[regex_telephone], 
        max_length=15, 
        blank=True,
        verbose_name="Téléphone"
    )
    
    # adresse utilisateur
    adresse = models.TextField(blank=True, verbose_name="adresse")
    ville = models.CharField(max_length=100, blank=True, verbose_name="Ville")
    code_postal = models.CharField(max_length=100, blank=True, verbose_name="Code_postal")
    
    # Statut du compte
    # is_active = models.BooleanField(default=True, verbose_name="Compte vérifié")
    email_verified = models.BooleanField(default=False, verbose_name="Email vérifié")
    phone_verified = models.BooleanField(default=False, verbose_name="Téléphone vérifié")

    # notification
    email_notifications = models.BooleanField(default=True, verbose_name="Notifications par email")
    sms_notifications = models.BooleanField(default=False, verbose_name="Notifications par SMS")
    

    #  Métadonnées
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")
    # last_login_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name="Dernière IP")
    
    # user_permissions = models.TextField()
    # groups = models.TextField()
    
    # on utilisera l'email comme identifiant de connexion
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

    @property
    def est_vendeur(self):
        """Vérifie si l'utilisateur est un vendeur"""
        return self.type_utilisateur == 'VENDEUR'
    
    @property
    def est_acheteur(self):
        """Vérifie si l'utilisateur est un acheteur"""
        return self.type_utilisateur == 'ACHETEUR'

    @property
    def get_is_active(self):
        return self.is_active
    
    def set_is_active(self, value):
        self.is_active = value
        
    def set_type_utilisateur(self, value):
        self.is_active = value

    def get_type_utilisateur(self, value):
        self.is_active = value
    """
    Profil étendu du vendeur
    Informations supplémentaires pour personnaliser l'expérience
    """
    
    # Photo de profil
    # avatar = models.ImageField(
    #     upload_to='avatars/', 
    #     blank=True, 
    #     null=True,
    #     verbose_name="Photo de profil"
    # )
    
    # Préférences
    bio = models.TextField(blank=True, max_length=500, verbose_name="Biographie")
    preferred_language = models.CharField(
        max_length=2, 
        choices=[('fr', 'Français'), ('en', 'English')],
        default='fr',
        verbose_name="Langue préférée"
    )

