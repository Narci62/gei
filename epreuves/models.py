from django.db import models
from django.contrib.auth import get_user_model
from pedagogie.models import Classe, Matiere, Theme, Lecon, Exercice

User = get_user_model()

class Epreuve(models.Model):
    professeur = models.ForeignKey(User, on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    trimestre = models.CharField(max_length=20)  # "1", "2", "3"
    themes = models.ManyToManyField(Theme)
    lecons = models.ManyToManyField(Lecon)
    date_creation = models.DateTimeField(auto_now_add=True)
    fichier_pdf = models.FileField(upload_to="epreuves_pdf/", null=True, blank=True)

    def __str__(self):
        return f"Epreuve {self.classe} - {self.matiere} ({self.date_creation.date()})"
