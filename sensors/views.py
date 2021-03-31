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


def get_charts(model, filters):
    fields_model = [f.name for f in model._meta.get_fields()]
    quaryset = model.objects.filter(**filters).values_list()
    df = pd.DataFrame(
        list(quaryset),
        columns=fields_model
    )

    return df


class ChartsData:

    def __init__(self, model, model_filter):
        self.model = model
        self.model_filter = model_filter
        self.df = None

    def get_dataframes(self):
        fields_model = [f.name for f in self.model._meta.get_fields()]
        quaryset = self.model.objects.filter(**self.model_filter).values_list()
        df = pd.DataFrame(list(quaryset), columns=fields_model)
        self.df = df

    def get_date_kwargs(self, df_key):
        self.get_dataframes()
        context_date = list(
            reversed([_.strftime("%H:%M:%S") for _ in self.df[df_key]]))
        return context_date

    def get_data_kwargs(self, df_key):
        self.get_dataframes()
        context_charts = list(reversed([_ for _ in self.df[df_key]]))
        return context_charts


def lk(request):
    request_sensor_id = 1
    building = 1

    if not request.GET:
        request_date = datetime.now().date()

    if "date" in request.GET:
        if not request.GET['date']:
            request_date = datetime.now().date()
        else:
            request_date = (datetime.strptime(
                request.GET['date'], '%Y-%m-%d')).date()

    filter_model_sensorsvalues = {
        "sensor_id": request_sensor_id,
        "pub_date__contains": request_date
    }
    filter_model_weather = {
        "building": building,
        "pub_date__contains": request_date
    }

    charts_sensors_values = ChartsData(
        SensorValues,
        filter_model_sensorsvalues
    )
    charts_weather_api = ChartsData(
        Weather,
        filter_model_weather
    )

    return render(
        request,
        'lk.html',
        {
            'labels': charts_sensors_values.get_date_kwargs('pub_date'),
            'data': charts_sensors_values.get_data_kwargs('value'),
            'labels_temp': charts_weather_api.get_date_kwargs('pub_date'),
            'data_temp': charts_weather_api.get_data_kwargs('temperature'),
            'labels_snow': charts_weather_api.get_date_kwargs('pub_date'),
            'data_snow': charts_weather_api.get_data_kwargs('snow')
        }
    )
