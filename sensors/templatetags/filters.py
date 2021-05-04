from django import template


from django.shortcuts import render, redirect, get_object_or_404
from sensors.models import (
    SensorValues, Sensor, Building,
    Weather,TemperatureSensorValues, TemperatureSensor,
    LeakSensor, LeakSensorValues
)


import pygal

register = template.Library()

def get_svgcharts(data):
    svg_urls = []
    x = 0
    for i in data:
        bar_chart = pygal.Bar()
        bar_chart.add('Данные протечек', i)
        url = f'media/chart{x}.svg'
        bar_chart.render_to_file(url)
        svg_urls.append(url)
        x+=1
    return svg_urls

@register.filter
def get_value(index, user):
    building = get_object_or_404(Building, owner=user)
    leaksensor = LeakSensor.objects.get(building_id=building)
    if leaksensor:
        leaksensorvalues = LeakSensorValues.objects.filter(sensor_id=leaksensor).first()
        leaksensorvalues = list(str(leaksensorvalues).strip('[ ]').split(','))
        leaksensorvalues = [int(item) for item in leaksensorvalues]

    message = 'Протечек не обнаружено'
    img = 'https://yt3.ggpht.com/a/AATXAJyRs3loFgPW0Ug_uo7gpng47u_vSWMZ5z-Tdgu7=s900-c-k-c0xffffffff-no-rj-mo'
    fill = "#00a806"

    if leaksensorvalues[index] > 30:
        message = 'Обнаружена протечка'
        img = "https://avatars.mds.yandex.net/get-zen_doc/168095/pub_5c0ab80c5970ce00a936fceb_5c0aba46006e0000abd77bfa/scale_1200"
        fill = "#bf2523"


    #Говнокод, потом приберу)))########################################
    list_value = []
    leaksensorvalues2 = LeakSensorValues.objects.all()[:4]
    for i in leaksensorvalues2:
        a = list(str(i).strip('[ ]').split(','))
        a = [int(item) for item in a]
        list_value.append(a)

    list_values = []
    y = 0
    for i in range(6):
        list_values.append((list_value[0][y], list_value[1][y], list_value[2][y], list_value[3][y]))
        y += 1

    charts_url = get_svgcharts(list_values)

    context = {
        "leaksensorvalues": leaksensorvalues[index],
        'message': message,
        'img': img,
        'fill': fill,
        'charts_url': charts_url[index]
    }
    return context
