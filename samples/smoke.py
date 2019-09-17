# coding=utf-8
import time
from nodes import Fan,Buzzer,Led,Co2Sensor,TemperatureSensor

def main():
    co2Sensor = Co2Sensor()
    temperatureSensor = TemperatureSensor()

    print('Detecting...')

    while True:
        co2Value = co2Sensor.value
        temperature = temperatureSensor.degree
        
        print('二氧化碳濃度:(%s) ppm' % (co2Value))
        print('溫度:(%s) °C' % (temperature))

        del co2Value
        del temperature
        time.sleep(3)

if __name__ == '__main__':
    main()
