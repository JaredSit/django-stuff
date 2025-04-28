from socket import fromshare
from django import forms

from views import challenges

from .models import *

class ChallengeForm(forms.modelForm):
    class Meta:
        model = Challenge
        fields = ['name', 'summary','flag_value','points']

