from django import forms
from django.contrib.auth.models import User


class UserSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "password"]
