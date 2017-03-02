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
from PIL import Image ,ImageEnhance
import subprocess
import tempfile

from image_processing.processor.engine.image_processor import *
from image_processing.processor.engine.processor_inputs import *
from image_processing.processor.engine.image_recognition import *
from image_processing.processor.utils import *

class ImageContentDetection(ImageTextDetection,ImagefaceRecognition,ImageContentRecognition):
    """
    image quality check
    """

    def __init__(self,image_path=None):
        if image_path:
            self.image_path = image_path
        else:
            self.image_path = '/Users/vikrant/vikrant/pics/test_d/good8.jpg'
        self.im_processor = ImageProcessingCalculations()
        self.im_processor_ops = ImageProcessingOps()
        self.tesseract_cmd = 'tesseract'

    @staticmethod
    def _get_image_obj(image_path=None):
        image_o = image_path
        return cv2.imread(image_o)

    def base_img_dimen(self,img_obj):
        self.height,self.width,_ = ImageProcessingInputsAndValidations().get_image_shape(img_obj)

    def content_metrecog(self,image_path=None):
        if image_path:
            org_img_obj = self._get_image_obj(image_path)
        else:
            org_img_obj = self._get_image_obj(self.image_path)

        img_text = self.text_recognition(org_img_obj)

        content_text = self.tensor_content_recognition(self.image_path)
        face_content = self.face_recognition(self.image_path)
        if len(face_content) > 0:
            has_face = True
        else:has_face=False
        img_text = img_text.replace('\n','')
        content_text = content_text.split('\n')
        content = {}
        for i,con in enumerate(content_text):
            content[str(i)] = con

        output = {'img_text':img_text,'content_text':content,'face_content':has_face}
        return output


       








if __name__ == '__main__':
    ImageContentDetection().content_metrecog()





