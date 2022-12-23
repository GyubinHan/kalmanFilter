import json
import csv
import os
import numpy as np
from pykalman import KalmanFilter as kf
from queue import PriorityQueue
import threading
import matplotlib.pyplot as plt
import time
from kafka import KafkaProducer
from kafka import KafkaConsumer
import json
from json import dumps, loads
import os
import matplotlib.pyplot as plt
import threading
from queue import PriorityQueue




producer = KafkaProducer(acks=0,
                         bootstrap_servers=['172.16.28.220:19092'],
                         compression_type='gzip',
                         value_serializer= lambda x: dumps(x).encode('utf-8'))


for i in range(3):
    data = {
        "time": i,
        "vehicles": [
        {
            "id": 991,
            "linkId": 90,
            "lane": 1,
            "location": 11.484880201098946,
            "speed": 41.113604245609324,
            "position": [
                -5747062.111932379,
                -967533.2282339633
            ]
        },
        {
            "id": 1032,
            "linkId": 102,
            "lane": 4,
            "location": 118.61874747898035,
            "speed": 42.51976193580154,
            "position": [
                -5747565.153118768,
                -967207.7858925589
            ]
        }]
        }
    producer.send("multithread-v1",data)
    
print("Producing done")


# global thread_que
thread_que = PriorityQueue()

consumer = KafkaConsumer("multithread-v1",
                         bootstrap_servers=['172.16.28.220:19092'],
                         group_id = 'multithread-group',
                         auto_offset_reset='earliest',
                         enable_auto_commit = True,
                         value_deserializer = lambda x: loads(x.decode('utf-8')))

thread_que = PriorityQueue()
for message in consumer:
 
    
    thread_que.put((message.value['time'],message.value['vehicles']))
    
    # print(thread_que.get())
    # thread_que.put(message.value)
    


    
