from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from sensors.models import SensorValues, Sensor, Building, Weather

from datetime import date, datetime
import pandas as pd
import numpy as np
from .forms import SensorForm, SensorSettingsForm, BuildingForm


def index(request):
    '''Вьюха отображения главной страницы'''
    # buildings = Building.objects.all()
    if request.method == 'POST':
        form = SensorForm(request.POST)
        # request_sensor_id = form.data['sens_uid']
        # print(request_sensor_id)
        if form.is_valid():
            # Обработка
            request_building = form.data['building']
            # form.save()  # сохранение  модели
            return redirect('lk2', request_building)
    else:
        form = SensorForm()

    data = 'привет'
    return render(request, 'index.html', context={'data': data,
                                                  'form': form
                                                  # 'buildings':buildings
                                                  })


def get_dataframes(model, filters):
    fields_model = [f.name for f in model._meta.get_fields()]
    quaryset = model.objects.filter(**filters).values_list()
    df = pd.DataFrame(list(quaryset), columns=fields_model)
    return df


def get_df_for_list(df, value, pub_date):
    date_value = []
    for i, k in zip(df[pub_date], df[value]):
        date_value.append({"x": i.strftime("%Y-%m-%d %H:%M:%S"), "y": k})
    return date_value


def lk(request):
    building = 1
    sens_id = [i for i in
               list(Sensor.objects.filter(building_id=building).values())]

    if not request.GET:
        request_date = datetime.now().date()
    if "date" in request.GET:
        if not request.GET['date']:
            request_date = datetime.now().date()
        else:
            request_date = (datetime.strptime(
                request.GET['date'], '%Y-%m-%d')).date()

    data = []
    for i in sens_id:
        filter_model_sensorsvalues = {
            "sensor_id": int(i['id']),
            "pub_date__contains": request_date
        }
        dataframe = get_dataframes(SensorValues, filter_model_sensorsvalues)
        x = get_df_for_list(dataframe, 'value', 'pub_date')
        data.append([i['sens_uid'], x])

    filter_model_weather = {
        "building": building,
        "pub_date__contains": request_date
    }
    dataframe_weather = get_dataframes(Weather, filter_model_weather)
    temperature = get_df_for_list(dataframe_weather, 'temperature', 'pub_date')
    snow = get_df_for_list(dataframe_weather, 'snow', 'pub_date')

    return render(
        request,
        'lk.html',
        {
            'data': data,
            'temperature': temperature,
            'snow': snow
        }
    )


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


def lk2(request, building_id):
    building = get_object_or_404(Building, id=building_id)
    sens_id = [i for i in
               list(Sensor.objects.filter(building_id=building_id).values())]

    print(sens_id)

    phone_number_form = PhoneForm(request.POST or None, instance=building)
    if phone_number_form.is_valid():
        phone_number_form.save(building)
        sensor_pk = phone_number_form.data['sensor']
        if sensor_pk:
            sensor = get_object_or_404(Sensor, pk=sensor_pk)
            value = phone_number_form.data['value']
            sensor.max_value = int(value)
            sensor.save()

    # if load_form.is_valid():
    #     sensor_pk = load_form.data['sensor']
    #     sensor = get_object_or_404(Sensor, pk=sensor_pk)
    #     value = load_form.data['value']
    #     sensor.max_value = int(value)

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
        data.append(
            [i['sens_uid'], charts_sensors_values.get_data_kwargs('value')])

    return render(
        request,
        'lk2.html',
        {
            # 'load_form': load_form,
            'phone_number_form': phone_number_form,
            'data': data,
            'labels': charts_sensors_values.get_date_kwargs('pub_date'),
            'labels_temp': charts_weather_api.get_date_kwargs('pub_date'),
            'data_temp': charts_weather_api.get_data_kwargs('temperature'),
            'labels_snow': charts_weather_api.get_date_kwargs('pub_date'),
            'data_snow': charts_weather_api.get_data_kwargs('snow')
        }
    )


def dashboard(request):
    try:
        building = get_object_or_404(Building, owner=request.user)
    except:
        return render(
            request,
            'misc/no_building.html', )

    sens_id = [i for i in
               list(Sensor.objects.filter(building_id=building).values())]



    if not request.GET:
        request_date = datetime.now().date()
    if "date" in request.GET:
        if not request.GET['date']:
            request_date = datetime.now().date()
        else:
            request_date = (datetime.strptime(
                request.GET['date'], '%Y-%m-%d')).date()

    data = []
    for i in sens_id:
        filter_model_sensorsvalues = {
            "sensor_id": int(i['id']),
            "pub_date__contains": request_date
        }
        dataframe = get_dataframes(SensorValues, filter_model_sensorsvalues)
        x = get_df_for_list(dataframe, 'value', 'pub_date')
        data.append([i['sens_uid'], x])

    filter_model_weather = {
        "building": building,
        "pub_date__contains": request_date
    }
    dataframe_weather = get_dataframes(Weather, filter_model_weather)
    temperature = get_df_for_list(dataframe_weather, 'temperature', 'pub_date')
    snow = get_df_for_list(dataframe_weather, 'snow', 'pub_date')

    return render(
        request,
        'dashboard.html',
        {
            'data': data,
            'temperature': temperature,
            'snow': snow
        }
    )


def snow_settings(request):
    try:
        building = get_object_or_404(Building, owner=request.user)
    except:
        return render(
            request,
            'misc/no_building.html', )

    sens_id = [i for i in
               list(Sensor.objects.filter(building_id=building).values())]

    sensor_settings_form = SensorSettingsForm(request.POST or None,
                                            instance=building)
    if sensor_settings_form.is_valid():
        sensor_settings_form.save(building)
        sensor_pk = sensor_settings_form.data['sensor']
        print(sensor_pk)
        if sensor_pk:
            sensor = get_object_or_404(Sensor, pk=sensor_pk)
            value = sensor_settings_form.data['value']
            if value:
                sensor.max_value = int(value)
                sensor.save()
            response_comand = sensor_settings_form.data['response_comand']
            print(response_comand)
            if response_comand:
                print(response_comand)
                sensor.response_comand = response_comand
                sensor.save()
    return render(
        request,
        'snow_settings.html',
        {
            # 'response_comand_form': response_comand_form,
            'sensor_settings_form': sensor_settings_form,
            # 'data': data,
            # 'temperature': temperature,
            # 'snow': snow
        }
    )


def building_settings(request):
    try:
        building = get_object_or_404(Building, owner=request.user)
    except:
        return render(
            request,
            'misc/no_building.html', )

    building_form = BuildingForm(request.POST or None, instance=building)
    if building_form.is_valid():
        building_form.save()
    return render(
        request,
        'building_settings.html',
        {
            # 'response_comand_form': response_comand_form,
            'building_form': building_form,
            # 'data': data,
            # 'temperature': temperature,
            # 'snow': snow
        }
    )