from django.shortcuts import get_object_or_404

from sensors.models import Building, Weather

from pyowm import OWM

owm = OWM('5b18d8916b3c773ff764614d3cd8f8c2')
mgr = owm.weather_manager()

def get_weather(building):
    building = get_object_or_404(Building, title=building)
    lat = building.coordinates_lat
    lon = building.coordinates_lon
    weather = mgr.weather_at_coords(lat, lon).weather
    temperature = weather.temperature('celsius')['temp']
    snow = weather.snow
    if snow:
        snow = weather.snow['1h']
    else:
        snow = 0


    return temperature, snow