from django.shortcuts import render
from sensors.models import SensorValues, Sensor, Building

from datetime import date, datetime
import pandas as pd
import numpy as np

from pyowm import OWM

owm = OWM('5b18d8916b3c773ff764614d3cd8f8c2')
mgr = owm.weather_manager()


def index(request):
    '''Вьюха отображения главной страницы'''
    # получаем список тегов из GET запроса
    # buildings = Building.objects.all()

    data = 'привет'
    return render(request, 'index.html', context={'data': data,
                                                  # 'buildings':buildings
                                                  })


# request_date = date(2021, 3, 29)

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


def lk2(request):
    '''тестовая - удалить'''
    moscow_lat = 55.75222
    moscow_lon = 37.615555
    weather = mgr.weather_at_coords(moscow_lat, moscow_lon).weather
    temperature = weather.temperature('celsius')['temp']
    snow = weather.snow
    if snow:
        snow = weather.snow['1h']
    else:
        snow = 0

    # snow1 = w.to_dict()
    # observation1 = mgr.one_call(lat= 69.22171367552382,lon=32.75035868403112)
    # dump_dict = observation1.forecast_hourly

    return render(request, 'lk2.html', {'temperature': temperature,
                                        'snow': snow,
                                        # 'rain': rain
                                        })
