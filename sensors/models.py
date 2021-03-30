from django.db import models



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

    coordinates_lat = models.FloatField(
        default=1,
        verbose_name='Долгота'

    )
    coordinates_lon = models.FloatField(
        default=1,
        verbose_name='Широта'
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
        ordering = ("-pub_date",)

    def __str__(self):
        return f'{self.value}'

    def get_value(self):
        return self.value


class Weather(models.Model):
    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        verbose_name='Объект'
    )

    # sensors = models.ManyToOneRel(Sensor)

    temperature = models.FloatField(
        verbose_name='Температура',
    )

    snow = models.FloatField(
        verbose_name='Снег',
    )

    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата показания',
    )


    class Meta:
        verbose_name = "Погодные данные"
        verbose_name_plural = "Погодные данные"
        ordering = ("-pub_date",)

    def get_temperature(self):
        return self.temperature

    def get_snow_info(self):
        return self.snow
