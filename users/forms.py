from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation

from .models import User, Address


class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given email, 
    first_name, last_name and password.
    """
    password1 = forms.CharField(
            label=_('Mot de passe'),
            widget=forms.PasswordInput
    )
    password2 = forms.CharField(
            label=_('Confirmation mot de passe'),
            widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = (User.USERNAME_FIELD, 'first_name', 'last_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("les mots de passe ne correspondent pas"))
        return password2

    def _post_clean(self):
        super()._post_clean()
        password = self.cleaned_data.get("password2")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error("password2", error)

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (User.USERNAME_FIELD, 'first_name', 'last_name')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class AddressCreateForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ('line1', 'line2', 'postal_code', 'city', 'phone')

