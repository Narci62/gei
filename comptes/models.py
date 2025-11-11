from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

class ProfesseurManager(BaseUserManager):
    def create_user(self, nom, prenom, telephone, password=None):
        if not nom or not prenom:
            raise ValueError("Nom et prénom sont obligatoires")
        user = self.model(
            nom=nom,
            prenom=prenom,
            telephone=telephone
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nom, prenom, telephone, password=None):
        user = self.create_user(nom, prenom, telephone, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Professeur(AbstractBaseUser, PermissionsMixin):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField(null=True, blank=True)
    lieu_naissance = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20, unique=True)
    date_inscription = models.DateTimeField(default=timezone.now)
    
    is_admin = models.BooleanField(default=False)  # ✅ Admin ou pas
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'telephone'
    REQUIRED_FIELDS = ['nom', 'prenom']

    objects = ProfesseurManager()

    def __str__(self):
        return f"{self.nom} {self.prenom}"
    

from django.utils import timezone
Professeur = get_user_model()

class DemandeAbonnement(models.Model):
    professeur = models.ForeignKey(Professeur, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=20)
    reference = models.CharField(max_length=100)
    date_demande = models.DateTimeField(auto_now_add=True)
    traitee = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.professeur} - {self.reference}"

class Abonnement(models.Model):
    professeur = models.OneToOneField(Professeur, on_delete=models.CASCADE)
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    actif = models.BooleanField(default=True)

    def est_valide(self):
        return self.actif and self.date_fin >= timezone.now().date()

    def jours_restants(self):
        return max(0, (self.date_fin - timezone.now().date()).days)

    def __str__(self):
        return f"{self.professeur} ({'Actif' if self.est_valide() else 'Expiré'})"