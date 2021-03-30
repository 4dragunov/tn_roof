from django.shortcuts import render
from sensors.models import SensorValues, Sensor, Building, Weather

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



def get_charts(model, filters, df_context):
    quaryset = model.objects.filter(**filters).values_list()
    df = pd.DataFrame(list(quaryset), **df_context)

    return df


def lk(request):
    request_sensor_id = 1
    building = 1

    if not request.GET:
        request_date = datetime.now().date()
        df = get_charts(
            SensorValues,
            {
                "sensor_id": request_sensor_id,
                "pub_date__contains": request_date
            },
            {
            'columns':['id', 'sensor', 'value', 'pub_date']
            }
        )

        df_temp = get_charts(
            Weather,
            {
                "building": building,
                "pub_date__contains": request_date
            },
            {
            'columns':['id', 'building', 'temperature', 'snow', 'pub_date']
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
            },
            {
            'columns':['id', 'sensor', 'value', 'pub_date']
            }
        )
        df_temp = get_charts(
            Weather,
            {
                "building": building,
                "pub_date__contains": request_date
            },
            {
            'columns':['id', 'building', 'temperature', 'snow', 'pub_date']
            }
        )


    labels = [_.strftime("%H:%M:%S") for _ in df['pub_date']]
    data = [_ for _ in df['value']]

    labels_temp = [_.strftime("%H:%M:%S") for _ in df_temp['pub_date']]
    data_temp = [_ for _ in df_temp['temperature']]

    labels_snow = [_.strftime("%H:%M:%S") for _ in df_temp['pub_date']]
    data_snow = [_ for _ in df_temp['snow']]



    return render(
        request,
        'lk.html',
        {
            'labels': sorted(labels),
            'data': sorted(data),
            'labels_temp':labels_temp,
            'data_temp':data_temp,
            'labels_snow':labels_snow,
            'data_snow':data_snow
        })

