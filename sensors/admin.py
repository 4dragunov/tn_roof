from django.contrib import admin

from .models import (
    Building,
    Sensor,
    SensorValues,
    Weather,
    TemperatureSensor,
    TemperatureSensorValues,
)


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'adress',
        'phone_number',
        'owner',
    )


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = (
        'sens_uid',
        'building',
        'values_count',
        'response_comand',
        'response_update_time',
        'max_value'
    )

    def values_count(self, obj):
        return SensorValues.objects.filter(sensor_id=obj).count()

    values_count.short_description = 'Число показаний'


@admin.register(TemperatureSensor)
class TemperatureSensorAdmin(admin.ModelAdmin):
    list_display = (
        'sens_uid',
        'building',
        'values_count',

    )

    def values_count(self, obj):
        return TemperatureSensorValues.objects.filter(sensor_id=obj).count()

    values_count.short_description = 'Число показаний'


@admin.register(SensorValues)
class SensorValuesAdmin(admin.ModelAdmin):
    list_display = (
        'sensor',
        'value',
        'pub_date',
    )

@admin.register(TemperatureSensorValues)
class TemperatureSensorValuesAdmin(admin.ModelAdmin):
    list_display = (
        'sensor',
        'value',
        'pub_date',
    )



@admin.register(Weather)
class WeatherAdmin(admin.ModelAdmin):
    list_display = (
        'building',
        'temperature',
        'snow',
        'pub_date',

    )
