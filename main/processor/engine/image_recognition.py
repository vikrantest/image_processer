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

from daily_scripts.utils import PSEReport
from image_processing.processor.engine.image_processor import *
from image_processing.processor.engine.processor_inputs import *
from image_processing.processor.utils import *

class ImageContentBase(ImageProcessingInputsAndValidations):
    """
    image quality check
    """

    def __init__(self,image_path=None):
        self.im_processor = ImageProcessingCalculations()
        self.im_processor_ops = ImageProcessingOps()
        self.tesseract_cmd = 'tesseract'

    def get_content_log_file(self):
        return "image_processing/log_files/content_logs.txt"

    def get_text_log_file(self):
        return "image_processing/log_files/text_logs.txt"


    def base_img_dimen(self,img_obj):
        self.height,self.width,_ = self.get_image_shape(img_obj)

    def get_text_blocks(self,bandw_obj,blank_img=False):
        denoise_obj =  self.im_processor_ops.remove_basic_noise(bandw_obj)
        rel,thres = self.im_processor_ops.get_otsu_binariation_thresh(bandw_obj)
        contours,cont_img,cont_blank_img = self.im_processor_ops.contours_lines(denoise_obj,thres,blank_img)
        dup_cont_blank_img = cont_blank_img
        cont_bounds = []
        _,_,cont_bounds = self.im_processor_ops.bound_contours(denoise_obj,cont_img,dup_cont_blank_img)
        return cont_img,cont_blank_img,cont_bounds

    def get_image_content(self,img_obj):
        a = tf.image.rgb_to_grayscale(img_obj, name=None)

    @staticmethod
    def create_temp():
        temp_file = tempfile.NamedTemporaryFile(prefix="tess_")
        return temp_file.name

    def run_shell_tesseract(self,command):
        f = open(self.get_content_log_file(), "w+")
        proc = subprocess.Popen(command,
            stderr=subprocess.PIPE)


        self.clean_temps(self.get_text_log_file())

        return (proc.wait(), proc.stderr.read())



    def image_text_extract(self):
        input_file , output_file = self.get_temp_io()
        image = Image.open(self.image_path)
        ImageEnhance.Contrast(image)
        image.save(input_file)
        output_file_log = '{}.txt'.format(output_file)
        image_text = ''
        
        command = [self.tesseract_cmd, input_file, output_file]
        result = self.run_shell_tesseract(command)
        with open(output_file_log) as f:
            img_text = f.read()
        self.clean_temps(input_file)
        self.clean_temps(output_file)
        print img_text

        return img_text


    @staticmethod
    def clean_temps(file_name):
        try:
            os.remove(file_name)
        except OSError:
            pass

    @staticmethod
    def get_temp_io():
        input_file = '{}.bmp'.format(ImageContentBase.create_temp())
        output_file = ImageContentBase.create_temp() 

        return input_file,output_file



class ImageTextDetection(ImageContentBase):

    def text_recognition(self,org_img_obj):
        rgb_obj = self.get_rgbscale_image(org_img_obj)
        grey_obj = self.get_greyscale_image(rgb_obj)

        self.base_img_dimen(org_img_obj)
        blank_img_obj = self.im_processor_ops.create_blank_image(self.height,self.width)
        cont_block,cont_block_on_blank,cont_bounds = self.get_text_blocks(grey_obj,blank_img = blank_img_obj)
        image_text = self.image_text_extract()
        blocks_dimens =  np.asarray(cont_bounds[:,2:4].T)
        return image_text

class ImagefaceRecognition(ImageContentBase):

    def training_classifier(self):
        self.face_cascade = cv2.CascadeClassifier('/Users/vikrant/vikrant/workspace/vikrant/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier('/Users/vikrant/vikrant/workspace/vikrant/opencv/data/haarcascades/haarcascade_eye.xml')


    def face_recognition(self,image_path):
        self.training_classifier()
        org_img_obj = self._get_image_obj(image_path)
        rgb_obj = self.get_rgbscale_image(org_img_obj)
        grey_obj = self.get_greyscale_image(rgb_obj)
        faces = self.face_cascade.detectMultiScale(grey_obj, 1.3, 5)
        for (x,y,w,h) in faces:
            img = cv2.rectangle(rgb_obj,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = grey_obj[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            eyes = self.eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        return faces

        # self.im_processor_ops.plot_image(img)

class ImageContentRecognition(ImageContentBase):

    def get_tensorflow_imagenet_path(self):
        imagenet_path = "/Users/vikrant/vikrant/virtualenvs/imp_eng/lib/python2.7/site-packages/tensorflow/models/image/imagenet/classify_image.py"

        return imagenet_path

    def tensor_content_recognition(self,image_file_path):
        imagenet_path = self.get_tensorflow_imagenet_path()
        command = ['python',imagenet_path,'--image_file',image_file_path]
        f = open(self.get_content_log_file(), "w+")
        subprocess.call(command, stdout=f)
        f.close()
        f = open(self.get_content_log_file(), "r+")
        image_content = f.read()
        f.close()

        self.clean_temps(self.get_content_log_file())

        return image_content





























"""
    def tensor_content_recognition(self,image_file_path):
        print "2121++++++++++++++"
        imagenet_path = self.get_tensorflow_imagenet_path()
        print image_file_path.split('/')[-1]
        input_file = '{0}/log_files/{1}.txt'.format(os.getcwd(),image_file_path.split('/')[-1])
        command = ['python',imagenet_path,'--image_file',image_file_path]
        print command
        data = ''
        print input_file
        f = open('input_file.txt','w+')
        cont_recog = subprocess.call(command,stdout=input_file)
        print f.close()
        print 'doneeeee++++++++++++++++++========================='
        print sdds
        self.clean_temps(input_file)
"""

    





