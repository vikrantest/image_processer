from botocore.client import Config
from kafka import KafkaConsumer,KafkaProducer
import boto3
import time
import sys
import json
import datetime
import os
import re
sys.path.append(os.getcwd())
from daily_scripts.utils import PSEReport
from image_processing.config import *
from image_processing.mains.utils import *
from image_processing.scoring_app.scoring_pars import ScoringInnerWeightDen


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        print cls,cls._instances
        return cls._instances[cls]


class GetImageScores(object):

	__metaclass__ = Singleton

	def __init__(self):
		self.score = 0
		self.score_weights = ScoringInnerWeightDen
		self.feat_weights = {'dimen':25,'laplacian':20,'aspect_ratio':15,'luminous':30,'content':10}
		

	def get_content_score(self):
		content_set = self.dataset['content_output']['content_text']
		for k,v in content_set.items():
			# uw_text = '( score = +\w+[0-9]+.+\w+[0-9]+)'
			uw_text = 'score = +\w+.+\w'
			w_point = re.findall(uw_text,v)
			if w_point:
				content_set[k] = v.replace('('+str(w_point[0])+')','')
		content_den = self.score_weights.get_content_weightage(content_set.values())
		return content_den

	def get_score(self,dataset):
		self.dataset = dataset
		if dataset:
			content_data = dataset['content_output']
			quality_data = dataset['quality_ouput']
		else:
			return 0
		if content_data:
			text_score = self.score_weights.get_is_text_weightage(content_data['img_text'])
			face_score = self.score_weights.get_is_face_weightage(content_data['face_content'])
			content_den = self.get_content_score()
			content_score = self.feat_weights['content']+content_den
			self.score = text_score+face_score+content_score
		else:
			text_score = face_score = 0

		if quality_data:
			b_and_w_score = self.score_weights.get_b_and_w_weightage(quality_data['is_grey_scale_image'])
			blank_score = self.score_weights.get_blank_weightage(quality_data['is_blank_image'])
			text_score = self.score_weights.get_is_text_weightage(content_data['img_text'])
			face_score = self.score_weights.get_is_face_weightage(content_data['face_content'])
			laplacian_den = self.score_weights.get_laplacian_weightage(quality_data['laplacian_value'])
			ap_den = self.score_weights.get_aspect_ratio_weightage(quality_data['ap_ratio'])
			luminous_den = self.score_weights.get_luminos_weightage(quality_data['luminance_value'])
			height_den = self.score_weights.get_image_size_weightage(quality_data['pixel_dimen'][0])
			ap_score = self.feat_weights['aspect_ratio']+ap_den
			luminous_score = self.feat_weights['luminous']+luminous_den
			laplacian_score = self.feat_weights['laplacian']+laplacian_den
			dimen_score = self.feat_weights['dimen']+height_den
			self.score = b_and_w_score+blank_score+ap_score+luminous_score+laplacian_score+dimen_score

		print self.score,'score+++++++++++++++++++++++++++++++++++11111'
		return self.score


