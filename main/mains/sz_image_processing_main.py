from botocore.client import Config
from kafka import KafkaConsumer,KafkaProducer
import boto3
import time
import sys
import json
import datetime
import os
import operator
import requests
import json
sys.path.append(os.getcwd())
from daily_scripts.utils import PSEReport
from image_processing.config import *
from image_processing.mains.utils import *
from image_processing.processor.img_pro_main import processor_main
from image_processing.scoring_app.scoring_eng import GetImageScores

class ImageProcessingConsumer(object):

    def __init__(self):
        topic_name = kafkaImageReadOutput['topic_ip']+'-image_process_init'
        self.producer = KafkaProducer()
        grp_id = 'image_process_initiator-' + str(int(time.time())) + '-' + 'image_processor'
        self.consumer = KafkaConsumer(topic_name,
                                      group_id=grp_id,
                                      auto_offset_reset='earliest',
                                      consumer_timeout_ms=900000,
                                      session_timeout_ms = 300000)
        session = boto3.Session(profile_name='prod')

        self.s3_prod = session.client('s3',config=Config(signature_version='s3v4'))
        self.db_client = PSEReport.client
        self.img_process_collection = 'sz_image_data_pro'
        self.image_score = GetImageScores()
        self.score_image = 'sz_images_score'
        self.sz_image_ordering_url = 'http://photosapi.service.stayzilla.com/pictures/rearrange'
        self.request_log_collection = 'sz_image_order_request_log'
        self.sz_cover_image_url = 'http://photosapi.service.stayzilla.com/pictures/set_cover_photo'

    def start_image_process(self,directory):
        processor_main(directory)

    def validate_processed_stays(self,stay_id):
        stay = self.db_client.sz_crawler.processed_stays_image.find({'sz_id':str(stay_id)})
        if stay:
            return True

    def log_processed_stays(self,stay_id):
        self.db_client.sz_crawler.processed_stays_image.update({'sz_id':str(stay_id)},{'sz_id':str(stay_id)},upsert = True)
        return True

    def get_processed_output(self,stay_id):
        stay_obj = self.db_client.sz_crawler[self.img_process_collection].find({'stay_id':str(stay_id)})
        if stay_obj:
            for data in stay_obj:
                return data

        return None

    def get_image_score(self,processed_data):
        score = self.image_score.get_score(processed_data)
        return score

    def save_image_score(self,dataset,score):
        dataset['score'] = score
        del dataset['_id']
        self.db_client.sz_crawler[self.score_image].update(dataset,dataset,upsert=True)


    def image_inputs(self):
        for message in self.consumer:
            response = message.value
            message_split = response.split('/')
            stay_id = message_split[0].split('-')[-1]
            stay_id = stay_id.strip()
            image_ids = message_split[2:]
            if str(stay_id) in ['77410']:
                is_processed = self.validate_processed_stays(stay_id)
                processed_data = self.get_processed_output(stay_id)
                if not is_processed or not processed_data:
                    print stay_id,'not prcoessed'
                    directory = UtilLib.get_images_from_s3(stay_id,image_ids,self.s3_prod)
                    self.start_image_process(directory)
                    self.log_processed_stays(stay_id)
                else:
                    print stay_id,'already processed+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
                # processed_data = self.get_processed_output(stay_id)
                # if processed_data:
                #     img_score = self.get_image_score(processed_data)
                #     self.save_image_score(processed_data,img_score)
                # os.remove(directory)
            else:
                print stay_id,'not processing dude...'
                pass

    def sz_stay_image_scoring(self):
        stays = self.db_client.sz_crawler[self.img_process_collection].find({})
        for stay in stays:
            if stay:
                img_score = self.get_image_score(stay)
                self.save_image_score(stay,img_score)

    def set_cover_image(self,hid,picid):
        payload = {"hid":int(hid),"picid":int(picid)}
        payload = json.dumps(payload)
        response = requests.post(self.sz_cover_image_url,payload,headers={"Content-Type": "application/json",})
        print response , 'cover image..........'
        self.db_client.sz_crawler[self.request_log_collection].insert({'response_text':'','response_code':'','stay_id':'','image_id':'','type':'cover photo'})
        return True

    def set_sz_stays_imgs_order(self,sorted_images,img_score_map,stay_id):
        for i,val in enumerate(sorted_images):
            picid = int(val.split('.')[0])
            if i==0:
                self.set_cover_image(stay_id,picid)
            payload = {"hid":int(stay_id),"picid":int(picid),"target":str(i)}
            payload = json.dumps(payload)
            response = requests.post(self.sz_image_ordering_url,payload,headers={"Content-Type": "application/json",})
            print response , 'rearrrange image order.........................'
            self.db_client.sz_crawler[self.request_log_collection].insert({'response_text':'','response_code':'','stay_id':'','image_id':'','type':'ordering'})


    def set_stay_image_ordering(self):
        stay_ids = self.db_client.sz_crawler.processed_stays_image.distinct('sz_id')
        stay_images_scores = self.db_client.sz_crawler[self.score_image].find({})
        stay_images_scores_order_map = {}
        for stay in stay_images_scores:
            if stay_images_scores_order_map.get(str(stay['stay_id']),None):
                stay_images_scores_order_map[str(stay['stay_id'])][stay['IMG']] = stay['score']
            else:
                stay_images_scores_order_map[str(stay['stay_id'])] = {stay['IMG']:stay['score']}
        for stay,scores in stay_images_scores_order_map.items():
            sorted_scores = sorted(scores.items(), key=operator.itemgetter(1),reverse=True)
            sorted_images = [x[0] for x in sorted_scores]
            self.set_sz_stays_imgs_order(sorted_images,scores,int(stay))






if __name__ == '__main__':
    ImageProcessingConsumer().image_inputs()
    ImageProcessingConsumer().sz_stay_image_scoring()
    ImageProcessingConsumer().set_stay_image_ordering()


