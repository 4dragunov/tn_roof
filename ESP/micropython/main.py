from machine import Pin
import time

led_pin = Pin(2,Pin.OUT)

while True:
    led_pin.on()
    print('on')
    time.sleep(1)
    led_pin.off()
    print('off')
    time.sleep(1)
