import os
import sys
import datetime
from pymongo import MongoClient
import boto3
import subprocess
from botocore.client import Config

class DBConstants(object):
    def __init__(self):
        self._host = 'localhost'
        self._username = ''
        self._passord = ''
        self.prod_bucket = 'sz-stay-pics-prod'
        self.aws_access_key_id='AKIAIHW4EZ4SUVNIDNZA'
        self.aws_secret_access_key='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'
        session = boto3.Session(profile_name='prod')

        self.s3_prod = session.client('s3',config=Config(signature_version='s3v4'))


class UtilLib(object):

    @staticmethod
    def create_temp_folder(subfolder = None):
        if 'img_process_temp' not in os.listdir('/tmp/'):
            subprocess.call(['mkdir','/tmp/img_process_temp'])
        tmp_dir = '/tmp/img_process_temp'
        if subfolder:
            subprocess.call(['mkdir','/tmp/img_process_temp/{}'.format(str(subfolder))])
            tmp_dir = '{}/{}'.format(tmp_dir,str(subfolder))
        return tmp_dir


class DBconnection(DBConstants):


    def mongo_connection(self,host='localhost'):
        if host == 'localhost':
            return MongoClient()
        else:
            uri = "mongodb://szbackend:szbackend123@172.31.2.58/szbackend?authMechanism=SCRAM-SHA-1"
            return MongoClient(uri)

    


