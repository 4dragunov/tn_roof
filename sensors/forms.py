from django import forms
from django.forms import ModelForm

from .models import Sensor, Building


class SensorForm(forms.Form):
    building = forms.ModelChoiceField(queryset=Building.objects.all())


class PhoneForm(forms.ModelForm):
    RESPONCE_COMANDS = (
        ('reboot', 'REBOOT'),
        ('tare', 'TARE'),
        ('ok', 'OK'),

    )

    sensor = forms.ModelChoiceField(queryset=Sensor.objects.all(),
                                    required=False)
    value = forms.IntegerField(required=False)


    response_comand = forms.ChoiceField(
        choices=RESPONCE_COMANDS,
        required=False)

    class Meta:
        model = Building
        fields = ('phone_number',)

#
# class ResponseComandForm(forms.ModelForm):
#     class Meta:
#         model = Sensor
#         fields = ('response_comand',)


# class Load_sms_form(forms.Form):
#     phone = forms.ModelForm
#     sensor = forms.ModelChoiceField(queryset=Sensor.objects.all())
#     value = forms.IntegerField()
