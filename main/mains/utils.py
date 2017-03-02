import os
import sys
import datetime
from pymongo import MongoClient
import boto3
import subprocess
from botocore.client import Config

class UtilLib(object):

    @staticmethod
    def create_temp_folder(subfolder = None):
        if 'img_process_temp' not in os.listdir('/tmp/'):
            subprocess.call(['mkdir','/tmp/img_process_temp'])
        tmp_dir = '/tmp/img_process_temp'
        if subfolder:
            stay_dir = '/tmp/img_process_temp/{}'.format(str(subfolder))
            if str(subfolder) not in os.listdir('/tmp/img_process_temp/'):
                subprocess.call(['mkdir','/tmp/img_process_temp/{}'.format(str(subfolder))])
            tmp_dir = '{}/{}'.format(tmp_dir,str(subfolder))
        return tmp_dir

    @staticmethod
    def get_images_from_s3(stay_id,img_ids,s3):
        tmp_dir = UtilLib.create_temp_folder(str(stay_id))
        for img in img_ids:
            dirs = list(str(stay_id))[-1]
            output_file = '{}/{}'.format(tmp_dir,img)
            key = '{}/{}/{}'.format(dirs,stay_id,img)
            print key
            if img not in os.listdir(tmp_dir):
                print 'download starts..................................'
                try:s3.download_file('sz-stay-pics-prod',key,output_file)
                except:
                    print key , '--------------------------error in finding 404 not found'
        return tmp_dir




