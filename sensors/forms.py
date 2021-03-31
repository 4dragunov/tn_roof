from django import forms
from django.forms import ModelForm

from .models import Sensor

class SensorForm(forms.Form):
    sens_uid = forms.ModelChoiceField(queryset=Sensor.objects.all())


