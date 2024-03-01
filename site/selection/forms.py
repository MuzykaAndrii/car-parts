from django import forms
from .models import SelectionRequest

class SelectionRequestForm(forms.ModelForm):
    class Meta:
        model = SelectionRequest
        fields = ['to_car', 'text']
