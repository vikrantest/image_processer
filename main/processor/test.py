#!/usr/bin/python

import datetime
import os
import sys
import time
import getopt
import cv2
import numpy as np
from matplotlib import pyplot as plt

sys.path.append(os.getcwd())
folder_names = ['101', '111', '115211', '115241', '115321', '115341', '115391', '115451', '118201', '120351', '120911', '122031', '1221', '122391\n11', '115121', '115221', '115271', '115331', '115351', '115441', '118141', '120341', '120721', '120941', '122061', '122381', '122401']
image_storage_path = "/Users/vikrant/vikrant/stay_images/"
temps = "/Users/vikrant/vikrant/pics/"

image_parent_folders = os.listdir(image_storage_path)
sub_folders = {}
image_parent_folders.remove('.DS_Store')
for m in image_parent_folders:
    sub_folders[image_storage_path+m] = os.listdir(image_storage_path+m)


images_maps = {}
for k,v in sub_folders.items():
    try:v.remove('.DS_Store')
    except:pass
    for x in v:
        images_maps[k+"/"+x] = os.listdir(k+"/"+x)


def main():
    input_images = [ k+"/"+x for k,v in images_maps.items() for x in v if x!='.DS_Store' ][10]
    print input_images
    for m in [input_images]:
        print m
        img = cv2.imread(m)
        print type(img),dir(img),img.size
        print img.item(10,10,2)# get red value
        print img.shape,img.dtype # get shape(rows,column,chanel) and datatype
        print cv2.split(img) #split images in bgr
        # print img[:,:,0] # b
        # print img[:,:,1] # g
        # print img[:,:,2] # r
        rows,cols,channels = img.shape
        roi = img[0:rows, 0:cols ] # get roi portion of image
        print cv2.Laplacian(img, cv2.CV_64F).var()

def check_blur():
    ifolder = 'blur/'
    print ifolder
    for m in os.listdir(temps+ifolder):
        print temps+ifolder+m,'++++++++++++++++++++',m
        img = cv2.imread(temps+ifolder+m)
        print ['image type','image size','red value','green value','blue value','laplacian value','image shape','image dtype','sobel filter X','Canney Edges']
        print type(img),img.size,img.item(10,10,2),img.item(10,10,1),img.item(10,10,0),cv2.Laplacian(img, cv2.CV_64F).var(),img.shape,img.dtype,cv2.Canny(img,100,200),cv2.calcHist(img,[0],None,[256],[0,256]) # , cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5) , cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)
        # print img.item(10,10,2)# get red value
        # print img.shape,img.dtype # get shape and datatype
        # rows,cols,channels = img.shape
        # roi = img[0:rows, 0:cols ] # get roi portion of image


def check_bac():
    ifolder = 'bac/'
    print ifolder
    for m in os.listdir(temps+ifolder):
        print temps+ifolder+m,'++++++++++++++++++++',m
        img = cv2.imread(temps+ifolder+m)
        print ['image type','image size','red value','green value','blue value','laplacian value','image shape','image dtype','sobel filter X','Canney Edges']
        print type(img),img.size,img.item(10,10,2),img.item(10,10,1),img.item(10,10,0),cv2.Laplacian(img, cv2.CV_64F).var(),img.shape,img.dtype,cv2.Canny(img,100,200),cv2.calcHist(img,[0],None,[256],[0,256]) # , cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5) , cv2.Sobel(img,cv2.CV_64F,0,1,ksize=5)
        # print type(img),dir(img),img.size
        # print img.item(10,10,2)# get red value
        # print img.shape,img.dtype # get shape and datatype
        # rows,cols,channels = img.shape
        # roi = img[0:rows, 0:cols ] # get roi portion of image
        # print cv2.Laplacian(img, cv2.CV_64F).var()

def check_blank():
    ifolder = 'blanks/'
    print ifolder
    for m in os.listdir(temps+ifolder):
        print temps+ifolder+m,'++++++++++++++++++++',m
        img = cv2.imread(temps+ifolder+m)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        print cv2.Laplacian(img, cv2.CV_64F).var()
        print ['image type','image size','red value','green value','blue value','laplacian value','image shape','image dtype','sobel filter X','Canney Edges']
        print type(img),img.size,img.item(10,10,2),img.item(10,10,1),img.item(10,10,0),cv2.Laplacian(img, cv2.CV_64F).var(),img.shape,img.dtype,
        # print type(img),dir(img),img.size
        # print img.item(10,10,2)# get red value
        # print img.shape,img.dtype # get shape and datatype
        # rows,cols,channels = img.shape
        # roi = img[0:rows, 0:cols ] # get roi portion of image
        # print cv2.Laplacian(img, cv2.CV_64F).var()








# check_blur()
# check_bac()
check_blank()