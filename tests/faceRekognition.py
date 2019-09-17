import os
import sys
import time
import boto3
from nodes import Led, Buzzer

led = Led()
buzzer = Buzzer()
collectionId='mycollection'

rek_client = boto3.client('rekognition', region_name = 'eu-west-1')

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
        os.system('cap 1280 960 8 1 -999 -1 -1')
        with open(path, 'rb') as image_binary:
            try:
                match_response = rek_client.search_faces_by_image(CollectionId=collectionId, Image={'Bytes': image_binary.read()}, MaxFaces=1, FaceMatchThreshold=90)
                if match_response['FaceMatches']:
                    led.on()
                    buzzer.off()
                    print('Hello, ',match_response['FaceMatches'][0]['Face']['ExternalImageId'])
                    print('Similarity: ',match_response['FaceMatches'][0]['Similarity'])
                    print('Confidence: ',match_response['FaceMatches'][0]['Face']['Confidence'])
                    break
                else:
                    led.off()
                    buzzer.on()
                    time.sleep(1)
                    buzzer.off()
                    print('No faces matched')
            except:
                print('No face detected')
        time.sleep(2)
        # Remove the file
        os.remove(path)
        print('Remove success')

if __name__ == '__main__':
    main()