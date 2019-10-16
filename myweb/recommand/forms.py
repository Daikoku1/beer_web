from django import forms
from .models import input_beer

class beerForm(forms.ModelForm):
    class Meta:
        model = input_beer
        fields = ['first', 'second', 'third']