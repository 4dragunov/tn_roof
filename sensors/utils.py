import os

from django.shortcuts import get_object_or_404
from twilio.rest import Client
from dotenv import load_dotenv
load_dotenv()
from sensors.models import Sensor
import logging
logging.basicConfig(filename="main.log", level=logging.DEBUG)

def check_max_value(sensor, value):

    max_value = sensor.max_value
    print(max_value)
    if value > max_value:
        text = str(f'Внимание!!! Значение датчика снеговой нагрузки'
                   f' {sensor.sens_uid} на '
                   f'объекте {sensor.building.title}'
                   f' {value} кг/м2. ' \
               f'Допустимая нагрузка {max_value} кг/м2')
        number = sensor.building.phone_number
        sms_sender(text, number)


def sms_sender(sms_text, number):
    print('Sms send complite!')
    account_sid = os.getenv('twilio_account_sid')
    auth_token = os.getenv('twilio_auth_token')
    # account_sid = {sectet.}
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=sms_text,
        from_=os.getenv('NUMBER_FROM'),
        to=number
    )
    return message.sid