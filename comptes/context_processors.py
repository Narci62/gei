from django.utils import timezone

def abonnement_restant(request):
    jours_restants = 0
    if request.user.is_authenticated and hasattr(request.user, 'date_fin_abonnement'):
        if request.user.date_fin_abonnement:
            delta = request.user.date_fin_abonnement - timezone.now().date()
            if delta.days > 0:
                jours_restants = delta.days
            else:
                jours_restants = 0
    return {'jours_restants': jours_restants}
