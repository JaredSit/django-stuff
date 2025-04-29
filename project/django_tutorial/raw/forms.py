from django import forms

from .views import *

from .models import *

class ChallengeForm(forms.ModelForm):
    class Meta:
        fields = ['name', 'summary','flag_value','points']

