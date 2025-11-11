from django.contrib import admin
from django.utils import timezone
from datetime import timedelta
from .models import Abonnement, DemandeAbonnement
from .sms import envoyer_sms  # Fichier sms.py à créer

@admin.action(description="Activer l’abonnement (30 jours)")
def activer_abonnement(modeladmin, request, queryset):
    for demande in queryset:
        if not demande.traitee:
            debut = timezone.now().date()
            fin = debut + timedelta(days=30)
            abonnement, _ = Abonnement.objects.update_or_create(
                professeur=demande.professeur,
                defaults={'date_debut': debut, 'date_fin': fin, 'actif': True}
            )
            envoyer_sms(
                demande.professeur.telephone,
                "Votre abonnement a été activé avec succès pour 30 jours. Merci !"
            )
            demande.traitee = True
            demande.save()

@admin.register(DemandeAbonnement)
class DemandeAbonnementAdmin(admin.ModelAdmin):
    list_display = ('professeur', 'telephone', 'reference', 'date_demande', 'traitee')
    actions = [activer_abonnement]

admin.site.register(Abonnement)




from django.contrib import admin
from .models import Professeur

admin.site.register(Professeur)