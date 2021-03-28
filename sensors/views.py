from django.shortcuts import render
from sensors.models import SensorValues, Sensor, Building

from datetime import datetime as dt

# Create your views here.
def index(request):
    '''Вьюха отображения главной страницы'''
    # получаем список тегов из GET запроса
    # buildings = Building.objects.all()

    data = 'привет'
    return render(request, 'index.html', context={'data': data,
                                                  # 'buildings':buildings
                                                  })


def lk(request):
    labels = []
    data = []
    
    queryset = SensorValues.objects.filter(sensor_id=1)
    for _ in queryset:
        labels.append((_.pub_date).strftime('%m/%d/%Y'))
        data.append(_.value)


    print(labels)
    print(data)
    return render(
        request,
        'lk.html',
        {
            'labels': labels,
            'data': data,
        })
