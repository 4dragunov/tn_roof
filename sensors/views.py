from django.shortcuts import render
from sensors.models import SensorValues, Sensor, Building

# Create your views here.
def index(request):
    '''Вьюха отображения главной страницы'''
    # получаем список тегов из GET запроса
    buildings = Building.objects.all()

    data = 'привет'
    return render(request, 'index.html', context={'data': data,
                                                  'buildings':buildings})
