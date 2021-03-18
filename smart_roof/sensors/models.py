from django.db import models

class Building(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='Название объекта',
        unique=True
    )

    def __str__(self):
        return self.title


class Sensor(models.Model):
    pin_number = models.CharField(
        max_length=100,
        verbose_name='Уникальный номер сенсора',
        unique=True
    )
    building = models.ForeignKey(Building,
                               null=True,
                               on_delete=models.SET_NULL,
                               related_name='objects',
                               verbose_name='Объект')

    def __str__(self):
        return self.pin_number


class Value(models.Model):

    sensor = models.ForeignKey(Sensor,
                               on_delete=models.CASCADE,
                               related_name='values',
                               verbose_name='Сенсор')
    value = models.FloatField(verbose_name='Показание',)
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата показания',
    )