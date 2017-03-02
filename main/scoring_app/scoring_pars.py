import os
import datetime
import sys
import re
import math
sys.path.append(os.getcwd())

class ContentKeyWords(object):

    @staticmethod
    def positive_stay_content_keywords():
        good_content_words = ['scenery', 'greenery', 'lake', 'seaside','mountain','sea','home','house','stay','hotel','motel',
                          'homestay','beachview','sunrise','sunset','bed','bedroom','wardrobe','balcony','quilt','comforter','couch','sofa'\
                          'sea','cloth','pillow','bedsheet','sliding door','library','dinning','kitchen','board','window shade',\
                          'bannister', 'banister', 'balustrade', 'balusters','comfort','day bed','closet','chiffonier','desk'\
                          'welcome mat','pot','flower pot','apron','patio','four poster','cradle']

        return good_content_words

    @staticmethod
    def average_stay_content_keywords():
        average_key_words = ['terrace','dressing table','lamp','night lamp','fire screen', 'fireguard','china cabinet', \
                           'china closet','rocking chair', 'rocker','television','laptop','fridge','blanket','painting']

        return average_key_words

    @staticmethod
    def bad_stay_content_keywords():
        bad_stay_keywords = ['bathroom','bathroom', 'bathtub', 'toilet', 'washbasin', 'handbasin','shower','restaurant', \
                          'eating house', 'eating place', 'eatery']

        return bad_stay_keywords





class ScoringInnerWeightDen(object):
    """
    get weightage scores from different params of images
    """


    @staticmethod
    def get_b_and_w_weightage(flag):
        if flag:
            return -10
        else:return 0

    @staticmethod
    def get_blank_weightage(flag):
        if flag:
            return -100
        else:
            return 0

    @staticmethod
    def get_is_text_weightage(text):
        text_len = len(text.strip())
        if text_len>0:
            return -10
        else:
            return 0

    @staticmethod
    def get_is_face_weightage(flag):
        if flag:
            return -10
        else:
            return 0

    @staticmethod
    def get_laplacian_weightage(val):
        if val > 3000:
            return 0
        elif 3000< val >2500:
            return -1
        elif 2500< val >2000:
            return -2
        elif 2000< val >1500:
            return -3
        elif 1500< val >1000:
            return -4
        elif 1000< val >750:
            return -5
        elif 750< val >550:
            return -6
        elif 550< val >350:
            return -7
        elif 350< val >150:
            return -8
        elif 150< val >50:
            return -9
        elif 50< val:
            return -10
        else:
            return 0

    @staticmethod
    def get_aspect_ratio_weightage(val):
        val = round(float(val),2)
        if val in [1.25,1.33,1.66,1.77]:
            return 0
        elif 1.77> val <2.00 or val == 1.00:
            return -3
        elif 0.75> val <1.00:
            return -6
        elif 0.33> val <0.75:
            return  -8
        elif val <0.33:
            return -9
        elif 1.00> val <1.25:
            return -4
        elif 2.00 > val <4.00:
            return -5
        elif val > 4.00:
            return -10
        elif 1.33 >val < 1.66:
            return -1
        elif 1.25 > val < 1.33:
            return -2
        else:
            return 0

    @staticmethod
    def get_luminos_histo_avg_weightage(val):
        if val > 7500:
            return 0
        elif 7500< val >6000:
            return -1
        elif 6000< val >5000:
            return -2
        elif 5000< val >4000:
            return -3
        elif 4000< val >2000:
            return -4
        elif 2000< val >1500:
            return -5
        elif 1500< val >1000:
            return -6
        elif 1000< val >500:
            return -7
        elif 500< val >300:
            return -8
        elif 300< val >100:
            return -9
        elif 100< val:
            return -10
        else:
            return 0

    @staticmethod
    def get_luminos_weightage(val):
        val = int(math.ceil(val))
        if val > 60:
            return 0
        elif 50< val >60:
            return -1
        elif 45< val >50:
            return -2
        elif 40< val >45:
            return -3
        elif 35< val >40:
            return -4
        elif 30< val >35:
            return -5
        elif 25< val >30:
            return -6
        elif 20< val >25:
            return -7
        elif 15< val >20:
            return -8
        elif 10< val >15:
            return -9
        elif 10< val:
            return -10
        else:
            return 0

    def get_noise_weightage():
        pass

    @staticmethod
    def get_image_size_weightage(height):
        if height in [1280,1366,1600,720,1024,640,320]:
            return 0
        elif height>4000:
            return -13
        elif 4000 > height >3600:
            return -9
        elif 3600 > height >1600:
            return -7        
        elif height < 320:
            return -9
        elif 1250 > height >1050:
            return -5
        else:return -3

    @staticmethod
    def get_content_weightage(content):
        good_content_words = ContentKeyWords.positive_stay_content_keywords()
        average_key_words = ContentKeyWords.average_stay_content_keywords()
        bad_key_words = ContentKeyWords.bad_stay_content_keywords()
        content_str = ' '.join(content)
        for words in good_content_words:
            if len(re.findall(words,content_str))>0:
                return 0

        for words in average_key_words:
            if len(re.findall(words,content_str))>0:
                return -6

        for words in bad_key_words:
            if len(re.findall(words,content_str))>0:
                return -10

        return -6







