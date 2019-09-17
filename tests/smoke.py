# coding=utf-8
import json
import time
from controller import BpiController
from nodes import Fan,Buzzer,Led,Co2Sensor,TemperatureSensor

bpiController = BpiController()
bpiController.mqttConnect()
buzzer = Buzzer()
led = Led()
fan = Fan()

def main():
    global fan
    global buzzer
    global led
    global bpiController

    print('Detecting...')
    co2Sensor = Co2Sensor()
    temperatureSensor = TemperatureSensor()

    while True:
        co2Value = co2Sensor.value
        temperature = temperatureSensor.degree

        print(co2Value)
        print(temperature)

        if co2Value >= 500 and temperature >= 35:
            print('開')
            errorMessage = '消防安全異常,二氧化碳濃度(%s), 溫度(%s)' % (co2Value, temperature)
            fan.on()
            led.on()
            buzzer.on()
        else:
            print('關')
            errorMessage = None
            led.off()
            buzzer.off()
            if fan.isOn():
                print('關風扇')
                fan.off()

        payload = {
            'smoke': {
                'reportInterval': 3,
                'co2': co2Value,
                'temperature': temperature,
                'fan': fan.getStatus(),
                'led': led.getStatus()
            }
        }
        if errorMessage:
            payload['smoke']['error'] = errorMessage

        # Report to aws Shadow
        bpiController.shadowUpdate(payload)
        # Report to sensor.live History DDB
        bpiController.reportHistory({
            'smoke': {
                'co2': co2Value,
                'temperature': temperature,
                'fan': fan.isOn(),
                'led': led.isOn()
            }
        })
        del co2Value
        del temperature
        time.sleep(3)

if __name__ == '__main__':
    main()
