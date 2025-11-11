from django.shortcuts import redirect
from django.utils import timezone
from .models import Abonnement

def abonnement_requis(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        try:
            abonnement = request.user.abonnement
            if not abonnement.est_valide():
                return redirect('comptes:souscrire_abonnement')
        except Abonnement.DoesNotExist:
            return redirect('comptes:souscrire_abonnement')

        return view_func(request, *args, **kwargs)
    return _wrapped_view
