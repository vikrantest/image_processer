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
from PIL import Image
sys.path.append(os.getcwd())
from daily_scripts.utils import PSEReport
from image_processing.processor.utils import ImageProcessUtils as IPU

class ImageProcessingInputsAndValidations(object):
    """
    image quality check
    """


    # self.color_code = {'red':2,'green':1,'blue':0}



    def get_img_size(self,image_obj):
        return image_obj.size

    def get_image_shape(self,image_obj):
        return image_obj.shape

    def get_image_pixels(self,image_obj):
        pass

    def get_image_dimen(self,pixel_dimen):
        return [IPU.pixels_to_cm(pixel_dimen[0]),IPU.pixels_to_cm(pixel_dimen[1])]

    def get_aspect_ratio(self,height,width):
        aspect_ratio = round(float(width)/float(height),3)
        return aspect_ratio

    def get_greyscale_image(self,image_obj):
        """
        convert image into grey scale
        """
        return cv2.cvtColor(image_obj, cv2.COLOR_RGB2GRAY)
        # return Image.open(self.image_path).convert('LA')

    def get_rgbscale_image(self,image_obj):
        """
        convert bgr to rgb scale
        """
        return cv2.cvtColor(image_obj, cv2.COLOR_BGR2RGB)

    def get_hsvscale_image(self,image_obj):
        """
        convert bgr to rgb scale
        """
        return cv2.cvtColor(image_obj, cv2.COLOR_RGB2HSV)


    def get_bgrscale_image(self,image_obj):
        """
        convert rgb to bgr scale
        """
        return cv2.cvtColor(image_obj, cv2.COLOR_RGB2BGR)

    def get_sobel_value(self,image_obj,axis):
        pass

    def get_color_gradient(self,image_obj,color):
        pass

    def get_image_gradient_data_type(self,image_obj):
        return image_obj.type

    def get_image_extesion(self,image_path):
        img_obj = Image.open(image_path)
        return img_obj.format

    def validate_color_image(self,image_obj):
        pass
