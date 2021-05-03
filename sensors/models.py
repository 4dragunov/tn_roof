from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Building(models.Model):
    image = models.ImageField(upload_to='sensors/buildings_plans/',
                              verbose_name='Изображение',
                              help_text='поле для рисунка',
                              null=True)
    #Координаты для создания SVG плана здания
    img_coordinates = models.JSONField(
        verbose_name='Координаты для плана',

    )
    owner = models.ForeignKey(User,
                              default=1,
                              on_delete=models.CASCADE,
                              related_name='buildings',
                              verbose_name='Заказчик')

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

    phone_number = models.CharField(
        max_length=12,
        verbose_name='Номер телефона инженера по эксплуатации',
        default='+79214462524'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Объект"
        verbose_name_plural = "Объекты"



class Sensor(models.Model):

    sens_uid = models.CharField(
        max_length=100,
        verbose_name='Уникальный номер датчика снега',
        unique=True,
    )

    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        verbose_name='Объект',
        related_name='sensor'
    )

    max_value = models.PositiveIntegerField(
        verbose_name='Значение для отправки уведомлений, кг/м2',
        default=200,
    )

    response_comand = models.CharField(
        default='ok',
        max_length=100,
        verbose_name='Команда для ответа с сервера',
    )

    response_update_time = models.PositiveIntegerField(
        default='60',
        verbose_name='Период обновления показателей, сек',
    )

    def __str__(self):
        return self.sens_uid

    def get_response_value(self):
        return self.response_comand

    def get_response_update_time(self):
        return self.response_update_time

    class Meta:
        verbose_name = "Датчик снега"
        verbose_name_plural = "Датчики снега"



class TemperatureSensor(models.Model):
    sens_uid = models.CharField(
        max_length=100,
        verbose_name='Уникальный номер датчика температуры',
        unique=True,
    )

    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        verbose_name='Объект',
        related_name='temperaturesensor'
    )


    def __str__(self):
        return self.sens_uid


    class Meta:
        verbose_name = "Датчик температуры"
        verbose_name_plural = "Датчики температуры"

class LeakSensor(models.Model):
    sens_uid = models.CharField(
        max_length=100,
        verbose_name='Уникальный номер системы протечки',
        unique=True,
    )

    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        verbose_name='Объект',
        related_name='leaksensor'
    )


    def __str__(self):
        return self.sens_uid


    class Meta:
        verbose_name = "Система мониторинга протечек"
        verbose_name_plural = "Системы мониторинга протечек"



class SensorValues(models.Model):
    sensor = models.ForeignKey(
        Sensor,
        on_delete=models.CASCADE,
        verbose_name='Датчик снега',
        related_name = 'sensorvalues'
    )

    value = models.FloatField(
        verbose_name='Показание датчика снега',
    )

    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата показания',
    )

    class Meta:

        verbose_name = "Показания датчиков снега"
        verbose_name_plural = "Показания датчиков снега"
        ordering = ("-pub_date",)

    def __str__(self):
        return f'{self.value}'

    def get_value(self):
        return self.value

class LeakSensorValues(models.Model):
    sensor = models.ForeignKey(
        LeakSensor,
        on_delete=models.CASCADE,
        verbose_name='Система мониторинга протечек',
        related_name='leaksensorvalues'
    )

    value = models.CharField(
        verbose_name='Показание системы мониторинга протечек',
        max_length=10000
    )

    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата показания',
    )

    class Meta:

        verbose_name = "Показание системы мониторинга протечек"
        verbose_name_plural = "Показания системы мониторинга протечек"
        ordering = ("-pub_date",)

    def __str__(self):
        return f'{self.value}'

    def get_value(self):
        return self.value

class TemperatureSensorValues(models.Model):
    sensor = models.ForeignKey(
        TemperatureSensor,
        on_delete=models.CASCADE,
        verbose_name='Датчик температуры',
        related_name='temperaturesensorvalues'
    )

    value = models.FloatField(
        verbose_name='Показание датчика температуры',
    )

    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата показания',
    )

    class Meta:

        verbose_name = "Показания датчика температуры"
        verbose_name_plural = "Показания датчиков температуры"
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


