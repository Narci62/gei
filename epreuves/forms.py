from django import forms
from pedagogie.models import Matiere, Classe, Trimestre, Theme, Lecon

class EpreuveForm(forms.Form):
    matiere = forms.ModelChoiceField(queryset=Matiere.objects.all(), label="Matière")
    classe = forms.ModelChoiceField(queryset=Classe.objects.all(), label="Classe")
    trimestre = forms.ModelChoiceField(queryset=Trimestre.objects.all(), label="Trimestre")
    themes = forms.ModelMultipleChoiceField(
        queryset=Theme.objects.none(),  # sera défini dans la vue
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    lecons = forms.ModelMultipleChoiceField(
        queryset=Lecon.objects.none(),  # sera défini dans la vue
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def __init__(self, *args, **kwargs):
        matiere = kwargs.pop('matiere', None)
        classe = kwargs.pop('classe', None)
        super().__init__(*args, **kwargs)

        if matiere and classe:
            self.fields['themes'].queryset = Theme.objects.filter(matiere=matiere, classe=classe)
            self.fields['lecons'].queryset = Lecon.objects.filter(theme__matiere=matiere, theme__classe=classe)

    def clean(self):
        cleaned_data = super().clean()
        themes = cleaned_data.get('themes')
        lecons = cleaned_data.get('lecons')

        if themes is None or not (1 <= len(themes) <= 3):
            self.add_error('themes', "Vous devez choisir entre 1 et 3 thèmes.")

        if lecons is None or not (2 <= len(lecons) <= 4):
            self.add_error('lecons', "Vous devez choisir entre 2 et 4 leçons.")
