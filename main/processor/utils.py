from botocore.client import Config
import boto3
import time
import os
import sys
import json
import datetime
import cv2
import csv
from matplotlib import pyplot as plt
import StringIO



def img_report_csv_header():
    header = ['Image','Content','Text','Face Presence','Is Black and White','Dimension in CM','Aspect ratio','Noise Count','Image Type',\
    'Histogram Peak','Laplacian','Luminance','Pixels Dimension','Is Blank','Histogram Mean']
    result_keys = ['Content_Text', 'Img_Text', 'Face_Content', 'Is_Grey_Scale_Image', 'Dimen', 'Ap_Ratio', 'Noise_Count', 'Image_Type',\
     'Colors_Histo_Peak', 'Laplacian_Value', 'Luminance_Value', 'Pixel_Dimen', 'Is_Blank_Image', 'Colors_Histo_Mean']
    return header , result_keys

class ImageProcessUtils(object):
    """
    ops related to image size , dimention and other params
    """

    idol_aspect_ratio = [1.0,1.25,1.6,1.777,1.333]
    _face_profile_path = "/Users/vikrant/vikrant/workspace/vikrant/opencv/data/haarcascades/"

    _face_profiles = ['haarcascade_eye.xml', 'haarcascade_eye_tree_eyeglasses.xml', 'haarcascade_frontalcatface.xml', 'haarcascade_frontalcatface_extended.xml', 'haarcascade_frontalface_alt.xml', 'haarcascade_frontalface_alt2.xml', 'haarcascade_frontalface_alt_tree.xml', 'haarcascade_frontalface_default.xml', 'haarcascade_fullbody.xml', 'haarcascade_lefteye_2splits.xml', 'haarcascade_licence_plate_rus_16stages.xml', 'haarcascade_lowerbody.xml', 'haarcascade_profileface.xml', 'haarcascade_righteye_2splits.xml', 'haarcascade_russian_plate_number.xml', 'haarcascade_smile.xml', 'haarcascade_upperbody.xml']

    @staticmethod
    def pixels_to_cm(pixels):
        return pixels * 2.54 / 96

    @staticmethod
    def plot_image(image_obj):
        plt.imshow(image_obj)
        plt.show()

    @staticmethod
    def save_content_in_txt_file(data_set,file_name):
        cont_obj = StringIO.StringIO()
        for datas in data_set:
            cont_obj.write('==================Image=====================')
            cont_obj.write('\n')
            # cont_obj.write('Image ---- {}'.format(datas['IMG']))
            del datas['IMG']
            cont_obj.write('\n')
            for k,v in datas.items():
                if 'id' not in k:
                    cont_obj.write('{} >>>>>>'.format(k.title()))
                    cont_obj.write('\n')
                    if type(v) != dict and type(v) == str:
                        cont_obj.write('{} ---------  {}'.format(k.title(),v))
                        cont_obj.write('\n')
                    elif type(v) == dict:
                        for x,y in v.items():
                            cont_obj.write('{} ---------  {}'.format(x.title(),y))
                            cont_obj.write('\n')
                cont_obj.write('\n')
            cont_obj.write('\n')
            cont_obj.write('\n')

        with open(file_name,'wb') as f:
            f.write(cont_obj.getvalue())

        # os.remove('output.txt')

    @staticmethod
    def save_content_in_csv_file(data_set,file_name):
        cont_obj = StringIO.StringIO()
        
        data_list = []

        for datas in data_set:
            da_li = [datas['IMG']]
            del datas['IMG']
            for k,v in datas.items():
                if k not in ['_id','image']:
                    if type(v) == dict:
                        for x,y in v.items():
                            da_li.append(str(y))

            data_list.append(da_li)

        with open(file_name,'wb') as csvfile:
            csv_writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
            headers , col_order = img_report_csv_header()
            csv_writer.writerow(headers)
            csv_writer.writerows(data_list)





