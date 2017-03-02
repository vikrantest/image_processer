from botocore.client import Config
from kafka import KafkaConsumer,KafkaProducer
import boto3
import time
import sys
import json
import datetime
import os
sys.path.append(os.getcwd())
from daily_scripts.utils import PSEReport
from image_processing.config import *
from image_processing.mains.utils import *
from image_processing.processor.img_pro_main import processor_main