from django.contrib import admin

from .models import (
    Building,
    Sensor,
    SensorValues,
    Sens
)


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = (
        'title',
    )


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = (
        'pin_number',
    )


@admin.register(Sens)
class ValueAdmin(admin.ModelAdmin):
    list_display = (
        'title',
    )


@admin.register(SensorValues)
class SensorValuesAdmin(admin.ModelAdmin):

    list_display = (
        'value',
        'sens_uid',
        'building',
        'pin_number',
        'pub_date',
        'sens'
    )
