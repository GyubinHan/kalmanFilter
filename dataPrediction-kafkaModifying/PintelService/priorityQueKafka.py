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
from queue import PriorityQueue



def json_reader(jsonname):
    with open(jsonname,'r') as f:
        json_data = json.load(f)
    return json_data
 

 
 
 
os.getcwd()
os.chdir("KafkaKalman/")
os.getcwd()



json_value1 = json_reader("newJsonTopicShort1.json")
json_value2 = json_reader("newJsonTopicShort2.json")
json_value3 = json_reader("newJsonTopicShort3.json")
json_value4 = json_reader("newJsonTopicShort4.json")
    

json_lst = []
json_lst.append(json_value1)
json_lst.append(json_value2)
json_lst.append(json_value3)
json_lst.append(json_value4)

producer = KafkaProducer(acks=0,
                         bootstrap_servers=['172.16.28.220:19092'],
                         compression_type='gzip',
                         value_serializer= lambda x: dumps(x).encode('utf-8'))

for i in json_lst:
    producer.send("priorityKalman-v1",i)
print("producing done")


que = PriorityQueue()
consumer = KafkaConsumer("priorityKalman-v1",
                         bootstrap_servers=['172.16.28.220:19092'],
                         group_id = 'priority-group',
                         auto_offset_reset = 'earliest',
                         enable_auto_commit= True,
                         value_deserializer = lambda x: loads(x.decode('utf-8')),
                         consume_timeout_ms = 1000
                         )
                        #  consumer_timeout_ms = 1000)


for message in consumer:
    que.put((message.value['time'],message.value['vehicles']))

    
