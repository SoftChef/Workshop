# coding=utf-8
import json
import time
from controller import BpiController
from nodes import Fan,Buzzer,Led,Co2Sensor

forceControl = False
isAlarm = False
bpiController = BpiController()
bpiController.mqttConnect()
buzzer = Buzzer()
led = Led()
fan = Fan()

# Custom Shadow callback
def shadowDeltaCallback(payload, responseStatus, token):
    global isAlarm
    global forceControl    
    global fan
    global bpiController

    # payload is a JSON string ready to be parsed using json.loads(...)
    # in both Py2.x and Py3.x
    payloadDict = json.loads(payload)
    print("++++++++DELTA++++++++++")
    print("property: " + str(payloadDict['state']))
    print("version: " + str(payloadDict['version']))
    print("+++++++++++++++++++++++\n\n")
    if not isAlarm and 'airQuality' in payloadDict['state'] and 'fan' in payloadDict['state']['airQuality']: 
        forceControl = True
        if payloadDict['state']['airQuality']['fan'] == 'on':
            print('遠端控制 : 開')
            fan.on()
            bpiController.shadowUpdate({
                'airQuality': {
                    'fan': 'on'
                }
            })
        elif payloadDict['state']['airQuality']['fan'] == 'off':
            print('遠端控制 : 關')
            fan.off()
            bpiController.shadowUpdate({
                'airQuality': {
                    'fan': 'off'
                }
            })
        else:
            print('未定義')
    else:
        print('目前不可控制')

def main():
    global isAlarm
    global forceControl
    global fan
    global led
    global bpiController

    print('Detecting...')
    bpiController.listenDeltaCallback(shadowDeltaCallback)
    co2Sensor = Co2Sensor()
    
    while True:
        co2Value = co2Sensor.value
        print('二氧化碳濃度:(%s) ppm' % (co2Value))
        if co2Value > 150:
            errorMessage = '二氧化碳濃度(%s)過高' % (co2Value)
            isAlarm = True
            led.on()
            fan.on()
        else:
            errorMessage = None
            isAlarm = False
            led.off()
            if not forceControl:
                if fan.isOn():
                    print('關風扇')
                    fan.off()

        payload = {
            'airQuality': {
                'reportInterval': 3,
                'co2': co2Value,
                'fan': fan.getStatus(),
                'led': led.getStatus()
            }
        }
        if errorMessage:
            payload['airQuality']['error'] = errorMessage

        # Report to aws Shadow
        bpiController.shadowUpdate(payload)
        # Report to sensor.live History DDB
        bpiController.reportHistory({
            'airQuality': {
                'co2': co2Value,
                'fan': fan.isOn(),
                'led': led.isOn()
            }
        })
        del co2Value
        time.sleep(3)

if __name__ == '__main__':
    main()