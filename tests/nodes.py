# coding=utf-8

import time
from grove.adc import ADC
from grove.gpio import GPIO
from grove.factory import Factory

class Led(GPIO):
    def __init__(self):
        super(Led, self).__init__(22, GPIO.OUT)
        self._status = 0 
        self.write(0)

    def on(self):
        self._status = 1
        self.write(1)

    def off(self):
        self._status = 0
        self.write(0)

    def isOn(self):
        return self._status == 1

    def getStatus(self):
        if self.isOn():
            return 'on'
        else:
            return 'off'

class Buzzer(GPIO):
    def __init__(self):
        super(Buzzer, self).__init__(16, GPIO.OUT)
        self._status = 0 
        self.write(0)

    def on(self):
        self._status = 1
        self.write(1)

    def off(self):
        self._status = 0
        self.write(0)

    def isOn(self):
        return self._status == 1

    def getStatus(self):
        if self.isOn():
            return 'on'
        else:
            return 'off'

class Fan():
    def __init__(self):
        print('Fan Init')
        self.fan = Factory.getGpioWrapper("Buzzer", 12)
        self._status = 0
        self.fan.off()

    def on(self):
        print('Fan Open')
        self._status = 1
        self.fan.on()
    
    def off(self):
        print('Fan Close')
        self._status = 0
        self.fan.off()

    def isOn(self):
        return self._status == 1

    def getStatus(self):
        if self.isOn():
            return 'on'
        else:
            return 'off'

class Co2Sensor:
    def __init__(self):
        self.channel = 0
        self.adc = ADC()

    @property
    def value(self):
        return self.adc.read(self.channel)

class LightSensor():
    def __init__(self):
        self.channel = 2
        self.adc = ADC()

    @property
    def brightness(self):
        return self.adc.read(self.channel)

class TemperatureSensor():
    def __init__(self):
        self.channel = 6
        self.sensor = Factory.getTemper("NTC-ADC", 6)

    @property
    def degree(self):
        return int(self.sensor.temperature)
