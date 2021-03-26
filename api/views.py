from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from rest_framework.serializers import RelatedField
from rest_framework import serializers

from sensors.models import *


def get_objects_id(model, filters):
    return model.objects.filter(**filters)[0].id


class DataSend(APIView):

    def post(self, request):
        sensor_uid = request.data['sensor_uid'] # получаем sensor_uid из json
        value = float(request.data['value'])  # получаем value из json
        zero_data = float(request.data['zero_data']) #  нуль для датчика
        is_debug = bool(int(request.data['is_debug']))
        sensor = get_object_or_404(Sensor, sens_uid=sensor_uid)
        if not is_debug: # если боевой режим
            if value < zero_data: # если значение около 0 (100г, 200...)
                # берем последнее значение из базы
                last_value_in_db = SensorValues.objects.filter(
                    sensor=sensor).latest('pub_date').get_value()
                last_value_in_db = float(last_value_in_db)
                # увеличиваем запись на последнее значение
                value = value + last_value_in_db
                # передаем последнее значение на весы
                last_value = value

        else: # если дебаг (не берем последние значения из базы)
            last_value = -1
        SensorValues.objects.create(sensor=sensor, value=value)
        return Response({'message': 'Success!',
                         'last_value': last_value})
