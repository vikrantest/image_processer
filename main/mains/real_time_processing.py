from botocore.client import Config
from kafka import KafkaConsumer,KafkaProducer
import boto3
import time
import sys
import json
import datetime
import os
sys.path.append(os.getcwd())
from image_processing.config import *
from image_processing.mains.utils import *


class RealTimeImageProcessingConsumer(object):

    def __init__(self):
        topic_name = kafkaRealTimeImageReadOutput['topic_ip']+'-image_process_init'
        print topic_name
        self.producer = KafkaProducer()
        grp_id = 'image_process_initiator-' + str(int(time.time())) + '-' + 'image_processor'
        self.consumer = KafkaConsumer(topic_name,
                                      group_id=grp_id,
                                      auto_offset_reset='earliest',
                                      consumer_timeout_ms=900000,
                                      session_timeout_ms = 300000)
        session = boto3.Session(profile_name='prod')

        self.s3_prod = session.client('s3',config=Config(signature_version='s3v4'))

    def start_requests(self):
        for message in self.consumer:
            print("Offset:" + str(message.offset) + ' ' + 'msg: ' + message.value.decode('utf-8'))
            response    = message.value
            message_split = response.split('/')
            stay_id = message_split[0].split('-')[-1]
            image_ids = message_split[2:]
            directory = UtilLib.get_images_from_s3(stay_id,image_ids,self.s3_prod)
            print directory,'directorydirectorydirectorydirectorydirectorydirectorydirectorydirectorydirectorydirectorydirectorydirectorydirectorydirectorydirectory'


if __name__ == '__main__':
    ImageProcessingConsumer().start_requests()