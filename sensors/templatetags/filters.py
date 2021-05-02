from django import template


from django.shortcuts import render, redirect, get_object_or_404
from sensors.models import (
    SensorValues, Sensor, Building,
    Weather,TemperatureSensorValues, TemperatureSensor,
    LeakSensor, LeakSensorValues
)

register = template.Library()


@register.filter
def get_value(index, user):
    building = get_object_or_404(Building, owner=user)
    leaksensor = LeakSensor.objects.get(building_id=building)
    if leaksensor:
        leaksensorvalues = LeakSensorValues.objects.filter(sensor_id=leaksensor).first()
        leaksensorvalues = list(str(leaksensorvalues).strip('[ ]').split(','))
        leaksensorvalues = [int(item) for item in leaksensorvalues]

    message = 'Всё в норме'
    img = 'https://yt3.ggpht.com/a/AATXAJyRs3loFgPW0Ug_uo7gpng47u_vSWMZ5z-Tdgu7=s900-c-k-c0xffffffff-no-rj-mo'
    fill = "#00ffff"

    if leaksensorvalues[index] > 1:
        message = 'ТЕЧЁЁЁЁЁТ'
        img = "https://avatars.mds.yandex.net/get-zen_doc/168095/pub_5c0ab80c5970ce00a936fceb_5c0aba46006e0000abd77bfa/scale_1200"
        fill = "#bf2523"

    context = {
        "leaksensorvalues": leaksensorvalues[index],
        'message': message,
        'img': img,
        'fill':fill
    }
    return context
