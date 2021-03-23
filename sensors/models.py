from django.db import models


# {
#     "building": "DOM1337",
#     "pin_number": "v12452434",
#     "count_sens":3,
#     "sensors":[
#         {
#         "sens": "FIRE_SENS",
#         "uid":"v2002",
#         "value":555
#     },
#     {
#         "sens": "WATER_SENS",
#         "uid":"v2000",
#         "value":4344
#     },
#     {
#         "sens": "SNOW_SENS",
#         "uid":"v2001",
#         "value":4444
#     }
#     ]
# }

# {
#     "building": "Pentagon",
#     "sensor_uid" : "x000001",
#     "value": "234.32"
# }
class Building(models.Model):
    title = models.CharField(
        unique=True,
        max_length=100,
        verbose_name='Название объекта'
    )

    adress = models.CharField(
        unique=True,
        max_length=200,
        verbose_name='Адрес объекта'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Объект"
        verbose_name_plural = "Объекты"


class Sensor(models.Model):
    sens_uid = models.CharField(
        max_length=100,
        verbose_name='Уникальный номер датчика',
        unique=True,
    )

    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        verbose_name='Объект'
    )

    def __str__(self):
        return self.sens_uid

    class Meta:
        verbose_name = "Датчик"
        verbose_name_plural = "Датчики"


class SensorValues(models.Model):
    sensor = models.ForeignKey(
        Sensor,
        on_delete=models.CASCADE,
        verbose_name='Датчик'
    )

    value = models.FloatField(
        verbose_name='Показание',
    )

    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата показания',
    )

    class Meta:
        verbose_name = "Показания датчиков"
        verbose_name_plural = "Показания датчиков"

    def __str__(self):
        return f'{self.sensor} ({self.value})'
