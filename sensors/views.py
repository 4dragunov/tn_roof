from django.shortcuts import render, redirect
from sensors.models import SensorValues, Sensor, Building, Weather

from datetime import date, datetime
import pandas as pd
import numpy as np
from .forms import SensorForm


def index(request):
    '''Вьюха отображения главной страницы'''
    # получаем список тегов из GET запроса
    # buildings = Building.objects.all()
    if request.method == 'POST':
        form = SensorForm(request.POST)
        # request_sensor_id = form.data['sens_uid']
        # print(request_sensor_id)
        if form.is_valid():
            # Обработка
            request_sensor_id = form.data['sens_uid']
            print(request_sensor_id)
            # form.save()  # сохранение  модели
            return redirect('lk2', request_sensor_id)
    else:
        form = SensorForm()

    data = 'привет'
    return render(request, 'index.html', context={'data': data,
                                                  'form': form
                                                  # 'buildings':buildings
                                                  })


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
    building = 1

    sens_id = [i for i in list(Sensor.objects.filter(building_id=building).values())]

    if not request.GET:
        request_date = datetime.now().date()

    if "date" in request.GET:
        if not request.GET['date']:
            request_date = datetime.now().date()
        else:
            request_date = (datetime.strptime(
                request.GET['date'], '%Y-%m-%d')).date()


    filter_model_weather = {
        "building": building,
        "pub_date__contains": request_date
    }

    charts_weather_api = ChartsData(
        Weather,
        filter_model_weather
    )

    data = []
    for i in sens_id:
        filter_model_sensorsvalues = {
            "sensor_id": int(i['id']),
            "pub_date__contains": request_date
        }
        charts_sensors_values = ChartsData(
            SensorValues,
            filter_model_sensorsvalues
        )
        data.append([i['sens_uid'],charts_sensors_values.get_data_kwargs('value')])


    return render(
        request,
        'lk.html',
        {
            'data': data,
            'labels': charts_sensors_values.get_date_kwargs('pub_date'),
            'labels_temp': charts_weather_api.get_date_kwargs('pub_date'),
            'data_temp': charts_weather_api.get_data_kwargs('temperature'),
            'labels_snow': charts_weather_api.get_date_kwargs('pub_date'),
            'data_snow': charts_weather_api.get_data_kwargs('snow')
        }
    )


def lk2(request, pk):
    if pk:
        request_sensor_id = pk
    else:
        request_sensor_id = 1
    building = 1
    charts_sensors_values_1 = []
    request_sensor_id = [1, 2]

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

    chart_labels = []
    chart_data = []
    for item in request_sensor_id:
        if not request.GET:
            request_date = datetime.now().date()

        if "date" in request.GET:
            if not request.GET['date']:
                request_date = datetime.now().date()
            else:
                request_date = (datetime.strptime(
                    request.GET['date'], '%Y-%m-%d')).date()

        filter_model_sensorsvalues = {
            "sensor_id": item,
            "pub_date__contains": request_date
        }
        charts_sensors_values = ChartsData(
            SensorValues,
            filter_model_sensorsvalues
        )

        chart_labels.append(charts_sensors_values.get_date_kwargs('pub_date'))
        chart_data.append((charts_sensors_values.get_data_kwargs(
            'value')))
    print(chart_labels)
    print(chart_data)

    return render(
        request,
        'lk2.html',
        {
            # 'labels': charts_sensors_values.get_date_kwargs('pub_date'),
            # 'data': charts_sensors_values.get_data_kwargs('value'),
            'labels': chart_labels,
            'data': chart_data,
            'labels_temp': charts_weather_api.get_date_kwargs('pub_date'),
            'data_temp': charts_weather_api.get_data_kwargs('temperature'),
            'labels_snow': charts_weather_api.get_date_kwargs('pub_date'),
            'data_snow': charts_weather_api.get_data_kwargs('snow')
        }
    )