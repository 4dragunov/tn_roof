from django.shortcuts import render
from sensors.models import SensorValues, Sensor, Building

from datetime import date
import pandas as pd
import numpy as np

# Create your views here.


def index(request):
    '''Вьюха отображения главной страницы'''
    # получаем список тегов из GET запроса
    # buildings = Building.objects.all()

    data = 'привет'
    return render(request, 'index.html', context={'data': data,
                                                  # 'buildings':buildings
                                                  })


# def objects_to_df(model, fields=None, exclude=None, date_cols=None, **kwargs):
#     if not fields:
#         fields = [field.name for field in model._meta.get_fields()]

#     if exclude:
#         fields = [field for field in fields if field not in exclude]
#     print(fields)
#     records = model.objects.filter(**kwargs).values_list(*fields)
#     df = pd.DataFrame(list(records), columns=fields)


#     if date_cols:
#         strftime = date_cols.pop(0)
#         for date_col in date_cols:
#             df[date_col] = df[date_col].apply(lambda x: x.strftime(strftime))

#     return df


def lk(request):

    request_date = date(2021, 3, 28)
    request_sensor_id = 1

    quaryset = SensorValues.objects.filter(sensor_id=request_sensor_id, pub_date__contains=request_date).values_list()
    df = pd.DataFrame(list(quaryset), columns=['id', 'sensor', 'value', 'pub_date'])

    labels = [_.strftime("%H:%M:%S") for _ in df['pub_date']]
    data = [_ for _ in df['value']]


    return render(
        request,
        'lk.html',
        {
            'labels': labels,
            'data': data,
        })
