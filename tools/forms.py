from django import forms


class EmailForm(forms.Form):
    email = forms.EmailField(label="Abonnez-vous pour Nos actualités",
            max_length=100,
            widget = forms.EmailInput(attrs={'class': 'form-control'}),
            help_text="votre email")
