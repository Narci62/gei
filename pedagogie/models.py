from django.db import models

# Classe (6e, 5e, etc.)
class Classe(models.Model):
    nom = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.nom

# Matière
class Matiere(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nom

# Trimestre
class Trimestre(models.Model):
    nom = models.CharField(max_length=20, unique=True)
    numero=models.IntegerField(default=0)
    

    def __str__(self):
        return self.nom

# Thème (lié à une classe et une matière)
class Theme(models.Model):
    nom = models.CharField(max_length=200)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nom}-{self.classe}"

# Leçon (liée à un thème)
class Lecon(models.Model):
    nom = models.CharField(max_length=200)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    trimestre=models.ForeignKey(Trimestre, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nom} - {self.theme}"

# Type d'exercice
TYPE_EXERCICE_CHOICES = [
    ("situation_probleme", "Situation Problème"),
    ("partie_a", "Partie A"),
    ("partie_b", "Partie B"),
    ("partie_c", "Partie C"),
    ("traditionnelle", "Exercice Traditionnel"),
]

# Exercice PDF
class Exercice(models.Model):
    fichier_tex = models.FileField(upload_to="exercices_tex/")
    type_exercice = models.CharField(max_length=30, choices=TYPE_EXERCICE_CHOICES)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    lecon = models.ForeignKey(Lecon, on_delete=models.CASCADE)
    trimestre = models.ForeignKey(Trimestre, on_delete=models.CASCADE)
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.theme.nom} - {self.lecon.nom} [{self.get_type_exercice_display()}]"
