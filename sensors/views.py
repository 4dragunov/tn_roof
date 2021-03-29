from django.shortcuts import render
from sensors.models import SensorValues, Sensor, Building

from datetime import date, datetime
import pandas as pd
import numpy as np


def index(request):
    '''Вьюха отображения главной страницы'''
    # получаем список тегов из GET запроса
    # buildings = Building.objects.all()

    data = 'привет'
    return render(request, 'index.html', context={'data': data,
                                                  # 'buildings':buildings
                                                  })


#request_date = date(2021, 3, 29)

def get_charts(model, filters):
    quaryset = model.objects.filter(**filters).values_list()
    df = pd.DataFrame(list(quaryset), columns=[
                      'id', 'sensor', 'value', 'pub_date'])

    return df


def lk(request):
    request_sensor_id = 1

    if not request.GET:
        request_date = datetime.now().date()
        df = get_charts(
            SensorValues,
            {
                "sensor_id": request_sensor_id,
                "pub_date__contains": request_date
            }
        )

    if "date" in request.GET:
        request_date = (datetime.strptime(
            request.GET['date'],
            '%Y-%m-%d'
        )).date()
        df = get_charts(
            SensorValues,
            {
                "sensor_id": request_sensor_id,
                "pub_date__contains": request_date
            }
        )

    labels = [_.strftime("%H:%M:%S") for _ in df['pub_date']]
    data = [_ for _ in df['value']]

    return render(
        request,
        'lk.html',
        {
            'labels': sorted(labels),
            'data': sorted(data),
        })
