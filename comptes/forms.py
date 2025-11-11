from django import forms
from .models import Professeur
from django.contrib.auth.forms import AuthenticationForm

class InscriptionForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Professeur
        fields = ['nom', 'prenom', 'date_naissance', 'lieu_naissance', 'telephone', 'password']

    def __init__(self, *args, **kwargs):
        super(InscriptionForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class ConnexionForm(AuthenticationForm):
    username = forms.CharField(label="Téléphone", widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Entrez votre numéro de téléphone'
    }))
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Entrez votre mot de passe'
    }))
    
    
    
    
    
from django import forms

class MotDePasseOublieForm(forms.Form):
    telephone = forms.CharField(
        label="Numéro de téléphone",
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez votre numéro de téléphone'
        })
    )

    lieu_naissance = forms.CharField(
        label="Lieu de naissance",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez votre lieu de naissance'
        })
    )

    nouveau_mot_de_passe = forms.CharField(
        label="Nouveau mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez un nouveau mot de passe'
        })
    )
