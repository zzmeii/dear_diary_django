from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField


class CustomAuthenticationForm(AuthenticationForm):
    username = None
    login = UsernameField(widget=forms.TextInput(attrs={"autofocus": True}))