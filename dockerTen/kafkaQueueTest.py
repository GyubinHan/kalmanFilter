import numpy as np
import pandas as pd
from pykalman import KalmanFilter as kf
import os
import csv
import matplotlib.pyplot as plt
import time
from kafka import KafkaProducer
from kafka import KafkaConsumer
import json
from json import dumps, loads
import os
import matplotlib.pyplot as plt
import copy 
import logging
from kafka.errors import KafkaError
from queue import PriorityQueue

sourceTopic =  'kalman-10-source'
targetTopic =  'kalman-10-target'
kafka_url =  ['172.16.28.218:19092','172.16.28.218:29092','172.16.28.218:39092','172.16.28.218:49092','172.16.28.218:59092']
# print(type(kafka_url))
url = '172.16.28.218:19092,172.16.28.218:29092,172.16.28.218:19092,172.16.28.218:19092,172.16.28.218:19092'
# print(url.split(','))
consumer_group =  'kafka-8'
kalman_number =  3
kalman_log = 'kalmanlog3.log'


consumer = KafkaConsumer(sourceTopic, group_id =consumer_group,bootstrap_servers=url.split(',')
                         ,auto_offset_reset='earliest',
                         value_deserializer = lambda x: loads(x.decode('utf-8')), enable_auto_commit=True, max_poll_interval_ms = 900000,
                         auto_commit_interval_ms=500)

que = PriorityQueue()


for message in consumer:
    que.put(message)
    if len(que) == 3:
        que.get()
        
        