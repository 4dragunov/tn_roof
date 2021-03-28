from django.shortcuts import render
from sensors.models import SensorValues, Sensor, Building

import datetime
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


def objects_to_df(model, fields=None, exclude=None, date_cols=None, **kwargs):
    if not fields:
        fields = [field.name for field in model._meta.get_fields()]

    if exclude:
        fields = [field for field in fields if field not in exclude]

    records = model.objects.filter(**kwargs).values_list(*fields)
    df = pd.DataFrame(list(records), columns=fields)

    if date_cols:
        strftime = date_cols.pop(0)
        for date_col in date_cols:
            df[date_col] = df[date_col].apply(lambda x: x.strftime(strftime))

    return df



def lk(request):
    labels = []
    data = []

    # queryset = SensorValues.objects.filter(sensor_id=1)
    # for _ in queryset:
    #     labels.append((_.pub_date).strftime('%m/%d/%Y-%H'))
    #     data.append(_.value)

    df = objects_to_df(SensorValues, date_cols=['%H', 'pub_date'])
    for i in range (0,24):
        date_filtred = (df[(df["pub_date"] == str(i))])
        averageNum = date_filtred.iloc[:, 2].mean()
        labels.append(i)
        if str(averageNum) == 'nan':
            data.append(0)
        else:
            data.append(averageNum)
        
    return render(
        request,
        'lk.html',
        {
            'labels': labels,
            'data': data,
        })
