# -*- coding: utf-8 -*-
import boto3

s3_client = boto3.client('s3')

collectionId = 'mycollection' #collection name

rek_client = boto3.client('rekognition')

bucket = 'hkpc-face-indexs-' + s3_client.meta.region_name #S3 bucket name

all_objects = s3_client.list_objects(Bucket = bucket)

list_response = rek_client.list_collections(MaxResults = 2)

if collectionId in list_response['CollectionIds']:
    rek_client.delete_collection(CollectionId = collectionId)

rek_client.create_collection(CollectionId = collectionId)

contents = []

if 'Contents' in all_objects:
    contents = all_objects['Contents']
if len(contents) == 0:
    print "================================================"
    print "Please upload your photo to %s Bucket" % (bucket)
    print "================================================"

for content in contents:
    collection_name,collection_image =content['Key'].split('/')
    if collection_image:
        label = collection_name
        print('indexing: ',label)
        image = content['Key']
        # 使用 rekognition API "index_faces" 
        index_response = rek_client.index_faces(CollectionId=collectionId,
                                Image={'S3Object':{'Bucket':bucket,'Name':image}},
                                ExternalImageId=label,
                                MaxFaces=1,
                                QualityFilter="AUTO",
                                DetectionAttributes=['ALL'])
        print('FaceId: ',index_response['FaceRecords'][0]['Face']['FaceId'])
