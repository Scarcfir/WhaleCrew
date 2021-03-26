from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "fadeIn second", "placeholder": "login", "id": "login"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "fadeIn third", "placeholder": "password", "id": "password"}))


class ForgotPassword(forms.Form):
    email = forms.CharField(
        widget=forms.TextInput(attrs={"class": "fadeIn second", "placeholder": "email", "id": "email"}))


class RegisterForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "fadeIn second", "placeholder": "login", "id": "login"}))
    email = forms.CharField(
        widget=forms.TextInput(attrs={"class": "fadeIn second", "placeholder": "email", "id": "email"}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "fadeIn third", "placeholder": "password", "id": "password"}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "fadeIn third", "placeholder": "password", "id": "password"}))

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password1'] != cleaned_data['password2']:
            raise ValidationError("Password doesn't match")



