from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import InscriptionForm, ConnexionForm
from .models import Professeur

def inscription_view(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            professeur = form.save(commit=False)
            professeur.set_password(form.cleaned_data['password'])
            professeur.save()
            return redirect('home')
    else:
        form = InscriptionForm()
    return render(request, 'inscription.html', {'form': form})

def connexion_view(request):
    if request.method == 'POST':
        form = ConnexionForm(request, data=request.POST)
        if form.is_valid():
            telephone = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, telephone=telephone, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = ConnexionForm()
    return render(request, 'connexion.html', {'form': form})

def deconnexion_view(request):
    logout(request)
    return redirect('home')



from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import MotDePasseOublieForm
from .models import Professeur

def mot_de_passe_oublie_view(request):
    if request.method == 'POST':
        form = MotDePasseOublieForm(request.POST)
        if form.is_valid():
            telephone = form.cleaned_data['telephone']
            lieu_naissance = form.cleaned_data['lieu_naissance']
            nouveau_mot_de_passe = form.cleaned_data['nouveau_mot_de_passe']

            try:
                user = Professeur.objects.get(
                    telephone=telephone,
                    lieu_naissance=lieu_naissance
                )
                user.set_password(nouveau_mot_de_passe)
                user.save()
                messages.success(request, "Mot de passe réinitialisé avec succès.")
                return redirect('connexion_view')
            except Professeur.DoesNotExist:
                messages.error(request, "Aucun utilisateur ne correspond aux informations fournies.")
    else:
        form = MotDePasseOublieForm()
    return render(request, 'mot_de_passe_oublie.html', {'form': form})




from django.shortcuts import render, redirect
from django.contrib import messages
from .models import DemandeAbonnement
from django.contrib.auth.decorators import login_required

@login_required
def souscrire_abonnement(request):
    professeur = request.user  # suppose que Professeur est lié à l'authentification

    if request.method == 'POST':
        telephone = request.POST.get('telephone')
        reference = request.POST.get('reference')
        DemandeAbonnement.objects.create(
            professeur=professeur,
            telephone=telephone,
            reference=reference
        )
        
        return render(request, 'demande_envoyee.html')

    return render(request, 'souscription.html')




# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import user_passes_test, login_required
from .models import DemandeAbonnement, Abonnement, Professeur

def envoyer_sms(numero, message):
    print(f"SMS à {numero}: {message}")
    # À remplacer par ton intégration avec un fournisseur SMS

def est_admin(user):
    return user.is_superuser

@user_passes_test(est_admin)
def liste_demandes_abonnement(request):
    demandes = DemandeAbonnement.objects.filter(traitee=False)
    return render(request, 'listes_demandes.html', {'demandes': demandes})

@user_passes_test(est_admin)
def activer_abonnement(request, demande_id):
    demande = get_object_or_404(DemandeAbonnement, id=demande_id)
    professeur = demande.professeur
    date_debut = timezone.now().date()
    date_fin = date_debut + timedelta(days=30)

    abonnement, created = Abonnement.objects.get_or_create(professeur=professeur)
    abonnement.date_debut = date_debut
    abonnement.date_fin = date_fin
    abonnement.actif = True
    abonnement.save()

    demande.traitee = True
    demande.save()

    #envoyer_sms(demande.telephone, "Votre abonnement a été activé pour 30 jours. Merci !")

    return redirect('comptes:liste_demandes_abonnement')

@user_passes_test(est_admin)
def rejeter_abonnement(request, demande_id):
    demande = get_object_or_404(DemandeAbonnement, id=demande_id)
    #envoyer_sms(demande.telephone, "Référence incorrecte. Contactez-nous via WhatsApp au 96 01 21 60.")
    demande.traitee = True
    demande.save()
    return redirect('comptes:liste_demandes_abonnement')
