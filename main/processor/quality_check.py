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
from image_processing.processor.engine.image_processor import *
from image_processing.processor.engine.processor_inputs import *

class ImageQualityFeatureDetection(ImageProcessingInputsAndValidations):
    """
    image quality check
    """

    def __init__(self,image_path=None):
        self.crawler_client = PSEReport.client
        if image_path:
            self.image_path = image_path
        else:
            # self.image_path = '/Users/vikrant/vikrant/pics/test_d/b_w1.jpg'
            self.image_path = '/tmp/img_process_temp/940/308386.jpg'
        self.im_processor = ImageProcessingCalculations()
        self.im_processor_ops = ImageProcessingOps()



    @staticmethod
    def _get_image_obj(image_path=None):
        image_o = image_path
        return cv2.imread(image_o)

    def base_img_dimen(self,img_obj):
        height,width,_ = self.get_image_shape(img_obj)
        aspect_ratio = self.get_aspect_ratio(height,width)
        image_dimension = self.get_image_dimen([height,width])
        self.height,self.width = height,width
        return aspect_ratio,image_dimension,[height,width]


    def quality_check(self,image_path=None):
        
        if image_path:
            org_img_obj = self._get_image_obj(image_path)
        else:
            org_img_obj = self._get_image_obj(self.image_path)
        rgb_obj = self.get_rgbscale_image(org_img_obj)
        grey_obj = self.get_greyscale_image(rgb_obj)
        #+++++++++++++++++++++++22444
        ap_ratio,dimen,pixel_dimen = self.base_img_dimen(rgb_obj)
        
        noise_hough_circles = ImageNoiseDetection(grey_obj).calculate_image_noise()
        noise_count = noise_hough_circles[1] - noise_hough_circles[0]

        image_type = self.get_image_extesion(self.image_path)
        is_grey_scale_image = self.im_processor.detect_black_white_image(rgb_obj,pixel_dimen)
        is_blank_image = self.im_processor.detect_blank_image(rgb_obj)
        laplacian_value = self.im_processor.calculate_Laplacian_value(org_img_obj)
        hsv_image = self.get_hsvscale_image(rgb_obj)
        luminance_value = self.im_processor.calculate_luminance_value(rgb_obj,pixel_dimen[0],pixel_dimen[1])
        histogram = self.im_processor.calculate_histogram_value(rgb_obj)
        # hough_img_obj = self.hough_circles()
        
        color = ('b','g','r')
        colors_histo = {'r':'red','b':'blue','g':'green'}
        colors_histo_mean = {}
        colors_histo_peak = {}
        for i,col in enumerate(color):
            histr = cv2.calcHist([rgb_obj],[i],None,[256],[0,256])
            # plt.plot(histr,color = col)
            # plt.xlim([0,256])
            
            c =  stats.mode(histr)
            counts = np.bincount(histr.flatten().astype(int))
            peak = np.argmax(counts)
            mean = np.mean(histr.flatten().astype(int))
            colors_histo_mean[colors_histo[col]] = mean
            colors_histo_peak[colors_histo[col]] = peak



        # plt.show()
        output = {}
        # ress = self.im_processor_ops.resize_image(rgb_obj,self.height,self.width,12,12)
        output['ap_ratio'] = ap_ratio
        output['dimen'] = dimen
        output['pixel_dimen'] = pixel_dimen
        output['image_type'] = image_type
        output['luminance_value'] = luminance_value
        output['is_blank_image'] = is_blank_image
        output['is_grey_scale_image'] = is_grey_scale_image
        output['laplacian_value'] = laplacian_value
        output['colors_histo_mean'] = colors_histo_mean
        output['colors_histo_peak'] = colors_histo_peak
        output['noise_count'] = noise_count

        return output










if __name__ == '__main__':
    ImageQualityFeatureDetection().quality_check()





