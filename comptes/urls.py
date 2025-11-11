from django.urls import path
from . import views

app_name = 'comptes'

urlpatterns = [
    path('inscription/', views.inscription_view, name='inscription_view'),
    path('connexion/', views.connexion_view, name='connexion_view'),
    path('deconnexion/', views.deconnexion_view, name='deconnexion_view'),
    path('mot-de-passe-oublie/', views.mot_de_passe_oublie_view, name='mot_de_passe_oublie_view'),
    path('abonnements/souscrire/', views.souscrire_abonnement, name='souscrire_abonnement'),
    path('admin/abonnements/', views.liste_demandes_abonnement, name='liste_demandes_abonnement'),
    path('admin/abonnements/activer/<int:demande_id>/', views.activer_abonnement, name='activer_abonnement'),
    path('admin/abonnements/rejeter/<int:demande_id>/', views.rejeter_abonnement, name='rejeter_abonnement'),
]
