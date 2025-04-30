from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from .models import *
class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = [
            'name',
            'summary',
            'flag_value',
            'points',
        ]
class FlagForm(forms.Form):
    flag_value = forms.CharField(max_length=100, label="Enter Flag")

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

class CustomLoginForm(AuthenticationForm):
    secret_code = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': "Enter Secret Code"}),
        help_text="Contact the admin if you don't have the secret code",
    )