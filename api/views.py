from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from rest_framework.serializers import RelatedField
from rest_framework import serializers

from sensors.models import *

from .weather_utils import get_weather

from sensors.utils import sms_sender, check_max_value

def get_objects_id(model, filters):
    return model.objects.filter(**filters)[0].id


class DataSend(APIView):

    def post(self, request):
        sensor_type = request.data['sensor_type'] # получаем тип датчика
        sensor_uid = request.data['sensor_uid']  # получаем sensor_uid из json
        value = float(request.data['value'])  # получаем value из json
        if sensor_type == 'snow':
            sensor = get_object_or_404(Sensor, sens_uid=sensor_uid)
            SensorValues.objects.create(sensor=sensor, value=value)
            check_max_value(sensor, value)
            response_comand = sensor.get_response_value()
            sensor.response_comand = 'ok'
            sensor.save()
        elif sensor_type == 'temperature':
            sensor = get_object_or_404(TemperatureSensor, sens_uid=sensor_uid)
            TemperatureSensorValues.objects.create(sensor=sensor, value=value)
            response_comand = 'ok'


        building = sensor.building


        temperature, snow = get_weather(building) #получаем данные прогноза
        Weather.objects.create(building=building,
                               temperature=float(temperature),
                               snow=float(snow)) # создаем запись в бд



        return Response({'message': 'Success!',
                         'response_comand': response_comand})


class DataGet(APIView):

    def post(self, request):
        sensor_uid = request.data['sensor_uid']
        sensor = get_object_or_404(Sensor, sens_uid=sensor_uid)
        last_value = SensorValues.objects.filter(
            sensor=sensor).latest('pub_date').get_value()
        return Response({'last_value': last_value})
