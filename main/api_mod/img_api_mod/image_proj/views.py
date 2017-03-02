from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pymongo import MongoClient
from image_proj.utils import *
from kafka import KafkaConsumer,KafkaProducer
from image_proj.config import kafkaAPIConfig

class SetStayImageProcessing(APIView):
    def __init__(self):
        self.storage_obj = DBconnection()
        self.img_client = self.storage_obj.mongo_connection()
        self.szbackend_client = self.storage_obj.mongo_connection('prod')
        self.s3 = boto3.client('s3', config=Config(signature_version='s3v4'))
        self.producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

    def get_stay_images(self,stay_id):
        stay_query = {'sz_id':int(stay_id)}
        fields = {'images':1,'_id':0}
        objects = self.szbackend_client.szbackend.stay.find(stay_query,fields).limit(1)
        return objects[0]

    def get(self,request):
        REQUEST_DATA = request.GET
        stay_id = REQUEST_DATA.get('stay_id',None)
        image_ids = REQUEST_DATA.get('image_ids',None)
        try:
            int(stay_id)
        except:
            return Response({'error':'Stay id should be integer.'},status=status.HTTP_400_BAD_REQUEST)

        if not stay_id:
            return Response({'error':'Stay id is mandatory for image processing.'},status=status.HTTP_400_BAD_REQUEST)
        else:
            img_objects = self.get_stay_images(stay_id)
            img_ids = [str(y['sz_id'])+'.'+str(y['ext']) for x in img_objects.values() for y in x]
        if image_ids:
            pro_img_ids = image_ids.split(',')
            img_ids = [x for x in img_ids if x.split('.')[0] in pro_img_ids]


        topic_name = '{}-image_process_init'.format(kafkaAPIConfig['topic_op'])
        key = 'stay_id-{}/imgs/{}'.format(stay_id,'/'.join(img_ids))
        # prod = KafkaProducer(bootstrap_servers=['localhost:9092'])
        # future = prod.send(topic_name, key)


        future = self.producer.send(topic_name, value=key)


        return Response({'message':'Image is under processing , do some useful in mean time.'},status=status.HTTP_200_OK)


class GetStayImageScores(APIView):
    def __init__(self):
        self.storage_obj = DBconnection()
        self.img_client = self.storage_obj.mongo_connection()
        self.szbackend_client = self.storage_obj.mongo_connection('prod')
        self.score_image = 'sz_images_score'

    def get(self,request):
        REQUEST_DATA = request.GET
        stay_id = REQUEST_DATA.get('stay_id',None)
        fields = REQUEST_DATA.get('fields',None)
        output = []
        if stay_id:
            query = {'stay_id':str(stay_id)}
            if fields:
                field = {'_id':0,'stay_id':1,'IMG':1,'score':1,'content_output':1,'quality_output':1}
                print "++++++++++++++++++++++++++"
                stay_images_scores = self.img_client.sz_crawler[self.score_image].find(query,field)
            else:
                field = {'_id':0,'IMG':1,'score':1}
                stay_images_scores = self.img_client.sz_crawler[self.score_image].find(query,field)
        else:
            return Response({'error':'Provide stay id for getting image scores.'},status=status.HTTP_400_BAD_REQUEST)

        if stay_images_scores:
            for m in stay_images_scores:
                print m
                output.append(m)


            return Response({'result':{'stay_id':str(stay_id),'image_scores':output}},status=status.HTTP_200_OK)
        else:
            return Response({'error':'Stay image scores not found.'},status=status.HTTP_404_NOT_FOUND)

