from django import forms
from django.forms import ModelForm

from .models import Sensor, Building


class SensorForm(forms.Form):
    building = forms.ModelChoiceField(queryset=Building.objects.all())


class SensorSettingsForm(forms.ModelForm):
    RESPONCE_COMANDS = (
        ('reboot', 'REBOOT'),
        ('tare', 'TARE'),
        ('ok', 'OK'),

    )

    sensor = forms.ModelChoiceField(queryset=Sensor.objects.all(),
                                    required=False,
                                    label='Уникальный номер датчика')



    response_comand = forms.ChoiceField(
        choices=RESPONCE_COMANDS,
        required=False,
        label='Cлужебные команды')

    class Meta:
        model = Sensor
        fields = ('max_value',)

class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ('title','adress','coordinates_lat','coordinates_lon',
                  'phone_number',)