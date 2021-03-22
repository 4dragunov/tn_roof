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
        print(request.data)

        building = request.data['building']
        sensor_uid = request.data['sensor_uid']
        value = request.data['value']

        print(building)
        print(sensor_uid)
        print(value)

        sensor = get_object_or_404(Sensor, sens_uid=sensor_uid)

        SensorValues.objects.create(sensor=sensor, value=value)

#
#         for _ in request.data['sensors']:
#             sens = _['sens']
#             sens_uid = _['uid']
#             value = _['value']
#
#             SensorValues.objects.create(
#                 sens_uid=sens_uid,
#                 value=value,
#                 building_id=get_objects_id(
#                     Building,
#                     {"title": building}
#                 ),
#                 pin_number_id=get_objects_id(
#                     Sensor,
#                     {"pin_number": pin_number}),
#                 sens_id=get_objects_id(
#                     Sens,
#                     {"title": sens}
#                 ),
#             )
#
        return Response({'message': 'Success!'})
#
