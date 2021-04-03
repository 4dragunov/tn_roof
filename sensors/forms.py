from django import forms
from django.forms import ModelForm

from .models import Sensor, Building

class SensorForm(forms.Form):
    building = forms.ModelChoiceField(queryset=Building.objects.all())


