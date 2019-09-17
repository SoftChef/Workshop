# -*- coding: utf-8 -*-

import os
import sys
import time
import boto3
from nodes import Led, Buzzer

led = Led()
buzzer = Buzzer()
collectionId='mycollection'

rek_client = boto3.client('rekognition')

width = '1280'
height = '960'
# File name is fixed, could't change
file = 'frame_%sx%s.jpg' % (width, height)

# File location 
currentLocation = os.getcwd()

# Path 
path = os.path.join(currentLocation, file) 

def main():
    while True:
        led.off()
        buzzer.off()
        os.system('cap 1280 960 8 1 -999 -1 -1')
        with open(path, 'rb') as image_binary:
            try:
                match_response = rek_client.search_faces_by_image(CollectionId=collectionId, Image={'Bytes': image_binary.read()}, MaxFaces=1, FaceMatchThreshold=90)
                if match_response['FaceMatches']:
                    led.on()
                    print('Hello, ',match_response['FaceMatches'][0]['Face']['ExternalImageId'])
                    print('Similarity: ',match_response['FaceMatches'][0]['Similarity'])
                    print('Confidence: ',match_response['FaceMatches'][0]['Face']['Confidence'])
                    break
                else:
                    buzzer.on()
                    print('No faces matched')
            except Exception as e:
                print('No face detected', str(e))
        time.sleep(2)
        # Remove the file
        os.remove(path)
        print('Remove success')

if __name__ == '__main__':
    main()