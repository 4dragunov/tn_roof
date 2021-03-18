from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from sensors.models import Building, Sensor, Value

class DataSend(APIView):

    def post(self, request):
        # print(request.data)
        building_title = request.data.get('building')
        building = Building.objects.get_or_create(title=building_title)
        device = request.data.get('device')
        device_number = request.data.get('device')[0]['number']
        sensor_count =  request.data.get('device')[1]['sensor_count']
        for i in range(2, sensor_count+2):
            sensor_value = request.data.get('device')[i][f'sensor_{i-1}']
            print(sensor_value)



        print(building)
        print(device)
        print(device_number)
        print(sensor_count)
        # sensor_id = request.data.get('sensor_id')
        # values = request.data.get('values')

        return Response({'message': 'Привет, мир!'})
