from django import forms


class EmailForm(forms.Form):
    email = forms.EmailField(label="votre email address",
            max_length=100,
            widget = forms.EmailInput(attrs={'class': 'form-control'}))
