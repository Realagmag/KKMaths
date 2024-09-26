from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label="Nazwa użytkownika", help_text=None)
    password1 = forms.CharField(
        label="Hasło", widget=forms.PasswordInput, help_text=None
    )
    password2 = forms.CharField(
        label="Potwierdź hasło", widget=forms.PasswordInput, help_text=None
    )

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]
