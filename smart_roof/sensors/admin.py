from django.contrib import admin
from .models import (
    Building,
    Sensor,
    Value
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
        'building'
    )
@admin.register(Value)
class ValueAdmin(admin.ModelAdmin):
    list_display = (
        'sensor',
        'value',
        'pub_date'
    )