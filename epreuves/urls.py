from django.urls import path
from .views import generer_epreuve,get_lecons_by_themes,mes_epreuves,exporter_epreuve_word

urlpatterns = [
    path("generer-epreuve/", generer_epreuve, name="generer_epreuve"),
    path("get-lecons-by-themes/", get_lecons_by_themes, name="get_lecons_by_themes"),
    path("epreuves/mes-epreuves/", mes_epreuves, name="mes_epreuves"),

   

]
