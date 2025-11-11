from django.urls import path
from . import views  # Importation des vues



urlpatterns = [
    path('', views.home, name='home'),  
    
]
