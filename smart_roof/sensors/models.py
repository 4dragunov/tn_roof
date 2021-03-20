from django.db import models


class Building(models.Model):
    title = models.CharField(
        unique=True,
        max_length=100,
        verbose_name='Название объекта'
    )

    def __str__(self):
        return self.title


class Sensor(models.Model):
    pin_number = models.CharField(
        max_length=100,
        verbose_name='Уникальный номер сенсора',
        unique=True,
    )

    def __str__(self):
        return self.pin_number


class Sens(models.Model):
    title = models.CharField(
        unique=True,
        max_length=100,
        verbose_name='Название датчика'
    )

    def __str__(self):
        return self.title


class SensorValues(models.Model):
    sens = models.ForeignKey(
        Sens,
        on_delete=models.CASCADE,
    )
    sens_uid = models.IntegerField(
        verbose_name='Уникальный идентификатор датчика',
    )
    value = models.BigIntegerField(
        verbose_name='Показание',
    )
    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
    )
    pin_number = models.ForeignKey(
        Sensor,
        on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата показания',
    )

    def __str__(self):
        return f'{self.sens} ({self.value})'
