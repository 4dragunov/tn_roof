import machine
import time
import gc

adc = machine.ADC(0)

def get_data():
    data = adc.read()
    print(data)
while True:
    try:
        get_data()
        gc.collect()
        time.sleep(1)
    except:
        print('error')

