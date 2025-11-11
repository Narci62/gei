# tasks.py
from celery import shared_task
from django.utils import timezone
from .models import Abonnement
from .sms import envoyer_sms

# tasks.py
@shared_task
def verifier_abonnements():
    from .models import Abonnement

    today = timezone.now().date()
    abonnements = Abonnement.objects.filter(actif=True)

    for ab in abonnements:
        jours = (ab.date_fin - today).days
        #if jours == 5:
            #envoyer_sms(ab.professeur.telephone, "Il vous reste 5 jours pour renouveler votre abonnement.")
        #elif jours <= 0:
            #ab.actif = False
            #ab.save()
            #envoyer_sms(ab.professeur.telephone, "Votre abonnement a expiré. Veuillez le renouveler.")
