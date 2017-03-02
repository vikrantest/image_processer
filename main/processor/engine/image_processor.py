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
import math
sys.path.append(os.getcwd())
from daily_scripts.utils import PSEReport
from matplotlib import pyplot as plt
from processor_inputs import ImageProcessingInputsAndValidations
from image_processing.processor.utils import *
    
class ImageProcessingCalculations(object):

    def __init__(self,image_obj=None):
        self.rgb_map = {'r':2,'g':1,'b':0}
        self._sigma=0.33
        self.rgb_map = {'0':'red','1':'green','2':'blue'}
        self.bgr_map = {'2':'red','1':'green','0':'blue'}
        self.hsv_constants = {'red': 0.27,'green':0.67,'blue':0.06}
        #np.dot(rgb[...,:3], [0.299, 0.587, 0.114])
        # #Standard
        # LuminanceA = (0.2126*R) + (0.7152*G) + (0.0722*B)
        # #Percieved A
        # LuminanceB = (0.299*R + 0.587*G + 0.114*B)
        # #Perceived B, slower to calculate
        # LuminanceC = sqrt( 0.241*R^2 + 0.691*G^2 + 0.068*B^2 )


    def calculate_hsv_value(self,image_obj,color):
        if 'green' in color:
            col = np.uint8([[[0,255,0 ]]])
        if 'red' in color:
            col = np.uint8([[[255,0,0 ]]])
        if 'blue' in color:
            col = np.uint8([[[0,0,255 ]]])

        hsv = cv2.cvtColor(col,cv2.COLOR_RGB2HSV)
        return hsv

    def calculate_histogram_value(self,image_obj,rgb = True,color=None):
        if rgb:
            histogram_map = {}
            if not color:
                for x,y in self.rgb_map.items():
                    histogram_value = cv2.calcHist([image_obj],[int(x)],None,[256],[0,256])
                    histogram_map[y] = histogram_value
            else:
                pass
        else:
            histogram_map['black&white'] = cv2.calcHist([image_obj],[0],None,[256],[0,256])


        return histogram_map

    def get_histogram_mean_mode(self,histogram_values):
        pass


    def calculate_luminance_value(self,image_obj,height,width,pixel = None):
        luminance = 0
        elem_count = 0
        if not pixel:
            for x in xrange(0,height):
                for y in xrange(0,width):
                    elem_count += 1
                    l_val = 0.00
                    for z in self.rgb_map.keys():
                        val = image_obj[x][y][int(z)]
                        hsv_const = self.hsv_constants[self.rgb_map[z]]
                        l_val += float(val)*hsv_const
                    luminance += l_val/3
        elif len(pixel) == 2:
            rgb = image_obj[pixel[0],pixel[1]]
            elem_count += 1
            l_val = 0.00
            for x in self.rgb_map.keys():
                val = rgb[int(x)]
                hsv_const = self.hsv_constants[self.rgb_map[x]]
                l_val += (float(val)*hsv_const)
            luminance += l_val/3

        else:
            luminance = 0

        luminance_average = round(float(luminance)/float(elem_count),3)

        return luminance_average

    def detect_blank_image(self,image_obj):
        imgray = cv2.cvtColor(image_obj,cv2.COLOR_RGB2GRAY)
        if np.count_nonzero(imgray) == 0:
            return True , 'Blank image'

        v = np.median(imgray)
        lower = int(max(0, (1.0 - self._sigma) * v))
        upper = int(min(255, (1.0 + self._sigma) * v))
        edges = ImageProcessingOps().get_canny_edges(image_obj)
        nonzero_edges = np.count_nonzero(edges)
        if nonzero_edges == 0:
            return True , 'Blank image'

        return False
        # ret,thresh = cv2.threshold(imgray,127,255,cv2.THRESH_TOZERO)
        # im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    def get_hough_circle(self,image_obj):
        circles = cv2.HoughCircles(image_obj,cv2.HOUGH_GRADIENT,5,20,param1=200,param2=50,minRadius=0,maxRadius=20)
        if type(circles) is np.ndarray:
            return np.uint16(np.around(circles))
        else:
            return 0

    def calculate_Laplacian_value(self,image_obj):
        image_obj = cv2.Laplacian(image_obj, cv2.CV_64F).var()
        return image_obj

    def find_contours(self,image_obj):
        image, contours, hierarchy = cv2.findContours(image_obj,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        return image,contours

    def detect_black_white_image(self,image_obj,pixel_dimen):# use numpy
        for x in xrange(0,pixel_dimen[0]):
            for y in xrange(0,pixel_dimen[1]):
                if image_obj[x][y][0]!=image_obj[x][y][1]!=image_obj[x][y][2]:
                    return False
        return True


class ImageProcessingOps(object):

    def __init__(self,image_obj=None):
        self._sigma=0.33
        self.im_processor = ImageProcessingCalculations()
        #apply filter to images
    # _sigma=0.33

    def resize_image(self,image_obj,height,width,h_constant,w_constant):
        res = cv2.resize(image_obj,(w_constant*width, h_constant*height), interpolation = cv2.INTER_CUBIC)
        return res

    def apply_standard_thresh(self,image_obj,thres_color=50,repl_color=255,THRESH_BINARY_INV = 0):
        return cv2.threshold(image_obj, thres_color, repl_color, THRESH_BINARY_INV)

    def apply_adaptive_thresh(self,image_obj):
        pass

    def get_otsu_binariation_thresh(self,image_obj):
        return cv2.threshold(image_obj,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)


    def remove_basic_noise(self,image_obj):
        image_obj = self.apply_gaussian_filter(image_obj)
        denoised_img = self.erode_dialate_images(image_obj)
        return image_obj

    def apply_gaussian_filter(self,image_obj):
        blur_image = cv2.GaussianBlur(image_obj,(5,5),0)
        return blur_image

    def erode_dialate_images(self,image_obj):
        image_obj = cv2.erode(image_obj, None, iterations=2)
        image_obj = cv2.dilate(image_obj, None, iterations=4)
        return image_obj

    def create_blank_image(self,height,width):
        blank_image = np.zeros((height,width,3), np.uint8)
        _,white_blank_image = self.apply_standard_thresh(blank_image,1,255,THRESH_BINARY_INV = 1)
        return white_blank_image

    def draw_contours(self,image_obj,contours,blank = False):
        img = cv2.drawContours(image_obj, contours, -1, (0,255,0), 1)
        return img

    def draw_contours_block(self,contour):
        img =  cv2.boundingRect(contour)
        return img

    def get_canny_edges(self,image_obj):
        v = np.median(image_obj)
        lower = int(max(0, (1.0 - self._sigma) * v))
        upper = int(min(255, (1.0 + self._sigma) * v))
        edges = cv2.Canny(image_obj,lower,upper)
        return edges

    def draw_hough_circles(self,image_obj,circles,blank = False):
        for i in circles[0,:]:
            # outer circle
            cv2.circle(image_obj,(i[0],i[1]),i[2],(0,255,0),1)
            # center of the circle
            cv2.circle(image_obj,(i[0],i[1]),2,(0,0,255),1)
        return image_obj

    def hough_circles(self,img_obj):
        circles = self.im_processor.get_hough_circle(img_obj)
        hough_img_obj = self.draw_hough_circles(img_obj,circles)
        # blank_hough_img_obj = self.draw_hough_circles(img_obj,circles,blank = True)
        return hough_img_obj,circles

    def contours_lines(self,img_obj,thres,blank_image=False):
        con_image,contours = self.im_processor.find_contours(thres)
        if blank_image is not None:
            cont_blank_img_obj = self.draw_contours(blank_image,contours)
        else:
            cont_blank_img_obj = None
        cont_img_obj = self.draw_contours(img_obj,contours)
        return contours,cont_img_obj,cont_blank_img_obj

    def bound_contours(self,img_obj,thres,blank_image=False,draw=False):
        con_image,contours = self.im_processor.find_contours(thres)
        cont_bounds = []
        for contour in contours:
            if blank_image is not None:
                [x,y,w,h] = self.draw_contours_block(contour)
                cont_bounds.append([x,y,w,h])
                if draw:cv2.rectangle(blank_image,(x,y),(x+w,y+h),(255,0,255),1)
            else:
                block_cont_blank_img_obj = None
            if draw:
                block_cont_img_obj = self.draw_contours_block(contour)
        cont_bounds = np.array(cont_bounds)
        return img_obj,blank_image,cont_bounds




class ImageNoiseDetection(ImageProcessingInputsAndValidations):
    """
    image recognition code
    """

    def __init__(self,image_obj):
        self.image_obj = image_obj
        self.im_processor = ImageProcessingCalculations()
        self.im_processor_ops = ImageProcessingOps()


    def calculate_image_noise(self):
        # ImageProcessUtils.plot_image(self.image_obj)
        circles,temp1 = self.im_processor_ops.hough_circles(self.image_obj)
        # ImageProcessUtils.plot_image(temp1)
        if type(circles) is not np.ndarray:
            circles_size = 0
        else:
            circles_size = circles.size

        denoise_img = self.im_processor_ops.remove_basic_noise(self.image_obj)
        new_circles = self.im_processor.get_hough_circle(denoise_img)
        new_circles,temp2= self.im_processor_ops.hough_circles(denoise_img)
        if type(new_circles) is not np.ndarray:
            new_circles_size = 0
        else:
            new_circles_size = new_circles.size

        # ImageProcessUtils.plot_image(temp2)

        return new_circles_size , circles_size

    





