# -*- coding:utf-8 -*-

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient,AWSIoTMQTTClient
import logging
import json
import time

class BpiController:
    def __init__(self):
        self.__host = 'axt811sti1q4w-ats.iot.us-east-2.amazonaws.com'
        self.__rootCA = '../certs/root-CA.crt'
        self.__certPem = '../certs/bpiController.cert.pem'
        self.__privateKey = '../certs/bpiController.private.key'
        self.__port = 8883
        self.__clientId = 'bpiControllerDevice'
        self.__thingName = 'bpiController'
        self.__thingType = 'Gateway'
        self.mqttClient = None
        self.basicMqttClient = None
        self.deviceShadowHandler = None

        # Configure logging
        # logger = logging.getLogger('AWSIoTPythonSDK.core')
        # logger.setLevel(logging.DEBUG)
        # streamHandler = logging.StreamHandler()
        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # streamHandler.setFormatter(formatter)
        # logger.addHandler(streamHandler)

        # Init AWSIoTMQTTShadowClient
        self.mqttClient = AWSIoTMQTTShadowClient(self.__clientId)
        self.mqttClient.configureEndpoint(self.__host, self.__port)
        self.mqttClient.configureCredentials(self.__rootCA, self.__privateKey, self.__certPem)

        # AWSIoTMQTTShadowClient configuration
        self.mqttClient.configureAutoReconnectBackoffTime(1, 32, 20)
        self.mqttClient.configureConnectDisconnectTimeout(10)  # 10 sec
        self.mqttClient.configureMQTTOperationTimeout(5)  # 5 sec

    def mqttConnect(self):
        # Connect to AWS IoT
        self.mqttClient.connect()
        # Create a deviceShadow with persistent subscription
        self.deviceShadowHandler = self.mqttClient.createShadowHandlerWithName(self.__thingName, True)

        return self.deviceShadowHandler

    def shadowUpdate(self, json_data):
        self.deviceShadowHandler.shadowUpdate(json.dumps({
            'state': {
                'reported': json_data
            }
        }), self.shadowUpdateCallback, 5)

    def reportHistory(self, json_data):
        if not isinstance(self.basicMqttClient, AWSIoTMQTTClient):
            print('Create AWSIoTMQTTClient')
            self.basicMqttClient = AWSIoTMQTTClient('bpiControllerReporter')
            self.basicMqttClient.configureEndpoint(self.__host, self.__port)
            self.basicMqttClient.configureCredentials(self.__rootCA, self.__privateKey, self.__certPem)
            self.basicMqttClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
            self.basicMqttClient.configureDrainingFrequency(2)  # Draining: 2 Hz
            self.basicMqttClient.configureConnectDisconnectTimeout(10)  # 10 sec
            self.basicMqttClient.configureMQTTOperationTimeout(5)  # 5 sec
            self.basicMqttClient.connect()

        topic = '@sensor.live/thing_types/%s/things/%s/history' % (self.__thingType, self.__thingName)
        self.basicMqttClient.publish(topic, json.dumps(json_data), 0)

    # Shadow callback
    def shadowUpdateCallback(self, payload, responseStatus, token):
        # payload is a JSON string ready to be parsed using json.loads(...)
        # in both Py2.x and Py3.x
        if responseStatus == 'timeout':
            print('Update request ' + token + ' time out!')
        if responseStatus == 'accepted':
            payloadDict = json.loads(payload)
            print('~~~~~~~~~~~~~~~~~~~~~~~')
            print('Update request with token: ' + token + ' accepted!')
            # print('property: ' + str(payloadDict))
            print('~~~~~~~~~~~~~~~~~~~~~~~\n\n')
        if responseStatus == 'rejected':
            print('Update request ' + token + ' rejected!')

    # Shadow delete callback
    def shadowDeleteCallback(self, payload, responseStatus, token):
        if responseStatus == 'timeout':
            print('Delete request ' + token + ' time out!')
        if responseStatus == 'accepted':
            print('~~~~~~~~~~~~~~~~~~~~~~~')
            print('Delete request with token: ' + token + ' accepted!')
            print('~~~~~~~~~~~~~~~~~~~~~~~\n\n')
        if responseStatus == 'rejected':
            print('Delete request ' + token + ' rejected!')

    # Listen on deltas
    def listenDeltaCallback(self, callback):
        if self.deviceShadowHandler is not None:
            self.deviceShadowHandler.shadowRegisterDeltaCallback(callback)
        else:
            raise Exception('deviceShadowHandler is None')

def main():
    bpiController = BpiController()
    bpiController.mqttConnect()
    # bpiController.shadowUpdate({
    #     "test": "hi"
    # })

    # Report sensor.live test
    # bpiController.reportHistory({
    #     "test": "hi"
    # })
    
    # Loop forever
    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()