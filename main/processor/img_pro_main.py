#!/usr/bin/python

from botocore.client import Config
import boto3
import time
import os
import sys
import json
import datetime
import cv2
import numpy as np
sys.path.append(os.getcwd())
from PIL import Image
from scipy import stats
import StringIO
from daily_scripts.utils import PSEReport
from image_processing.processor.engine.image_processor import ImageNoiseDetection,ImageProcessingOps,ImageProcessingCalculations
from image_processing.processor.engine.processor_inputs import ImageProcessingInputsAndValidations
from image_processing.processor.engine.image_recognition import ImageContentRecognition,ImagefaceRecognition,ImageTextDetection
from image_processing.processor.quality_check import ImageQualityFeatureDetection
from image_processing.processor.content_check import ImageContentDetection
from image_processing.processor.utils import *

class ImageProcessAndContent(ImageQualityFeatureDetection,ImageContentDetection):
    def __init__(self,image_path=None):
        if not image_path:
            self.image_path = '/Users/vikrant/vikrant/pics/noisy/6.jpeg'
        else:
            self.image_path = image_path
        self.quality_lib = ImageQualityFeatureDetection(image_path)
        self.content_lib = ImageContentDetection(image_path)
        self.crawler_client = PSEReport.client
        self.img_process_collection = 'sz_image_data_pro'

    def get_img_content(self):
        content_output = self.content_lib.content_metrecog()
        quality_ouput = self.quality_lib.quality_check()
        output = {'content_output':content_output,'quality_ouput':quality_ouput}
        output['image'] = {'name':self.image_path.split('/')[-1]}
        # self.save_to_mongo(output)

        return output

    def save_to_mongo(self,data_set):
        self.crawler_client.sz_crawler[self.img_process_collection].insert(data_set)


def processor_main(image_dir):
    file_obj = StringIO.StringIO()
    output_list = []
    for m in os.listdir(image_dir):
        # if 'text' in m:
        if len(m.split('.')) == 2:
            images = '{}/{}'.format(image_dir,m)
            print 'Processing image {} in progress................................'.format(m)
            main_processor = ImageProcessAndContent(images)
            output = main_processor.get_img_content()
            output['IMG'] = m
            stay_id = image_dir.split('/')[-1]
            output['stay_id'] = stay_id
            output_list.append(output)
            main_processor.save_to_mongo(output)
            print 'Processing image {} is done ................................'.format(m)
        # print len(output)
        # ImageProcessUtils.save_content_in_csv_file(output_list,temp_log)






# use string IO whereevr files are used
if __name__ == '__main__':
    output = processor_main()

