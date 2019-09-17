# coding=utf-8
import json
import time
from controller import BpiController
from nodes import Buzzer,Led,LightSensor,TemperatureSensor

forceControl = False
isAlarm = False
bpiController = BpiController()
bpiController.mqttConnect()
led = Led()
buzzer = Buzzer()

# Custom Shadow callback
def shadowDeltaCallback(payload, responseStatus, token):
    global isAlarm
    global forceControl
    global led
    global bpiController

    # payload is a JSON string ready to be parsed using json.loads(...)
    # in both Py2.x and Py3.x
    payloadDict = json.loads(payload)
    print("++++++++DELTA++++++++++")
    print("property: " + str(payloadDict['state']))
    print("+++++++++++++++++++++++\n\n")
    if not isAlarm and 'lightRegulator' in payloadDict['state'] and 'led' in payloadDict['state']['lightRegulator']: 
        forceControl = True
        if payloadDict['state']['lightRegulator']['led'] == 'on':
            print('遠端控制 : 開')
            led.on()
            bpiController.shadowUpdate({
                'lightRegulator': {
                    'led': 'on'
                }
            })
        elif payloadDict['state']['lightRegulator']['led'] == 'off':
            print('遠端控制 : 關')
            led.off()
            bpiController.shadowUpdate({
                'lightRegulator': {
                    'led': 'off'
                }
            })
        else:
            print('未定義')
    else:
        print('目前不可控制')

def main():
    global isAlarm
    global forceControl
    global buzzer
    global led
    global bpiController
    
    print('Detecting...')
    bpiController.listenDeltaCallback(shadowDeltaCallback)
    lightSensor = LightSensor()
    temperatureSensor = TemperatureSensor()

    while True:
        brightness = lightSensor.brightness
        temperature = temperatureSensor.degree

        print('亮度:(%s)' % (brightness))
        print('溫度:(%s) °C' % (temperature))

        if temperature >= 27:
            errorMessage = '燈泡溫度(%s)過高' % (temperature)
            isAlarm = True
            buzzer.on()
            time.sleep(0.5)
            buzzer.off()
        else:
            errorMessage = None
            isAlarm = False
            buzzer.off()
            
        if brightness < 100 and temperature < 27:
            led.on()
        else:
            if not forceControl:
                led.off()

        payload = {
            'lightRegulator': {
                'reportInterval': 3,
                'led': led.getStatus(),
                'temperature': temperature,
                'brightness': brightness
            }
        }
        if errorMessage:
            payload['lightRegulator']['error'] = errorMessage

        # Report to aws Shadow
        bpiController.shadowUpdate(payload)
        # Report to sensor.live History DDB
        bpiController.reportHistory({
            'lightRegulator': {
                'led': led.isOn(),
                'temperature': temperature,
                'brightness': brightness
            }
        })
        time.sleep(3)

if __name__ == '__main__':
    main()
