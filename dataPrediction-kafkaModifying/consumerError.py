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
from kafka import errors
import time


producer = KafkaProducer(acks=0,
                         compression_type = 'gzip',
                         bootstrap_servers=['172.16.28.220:19092'],
                         value_serializer= lambda x: dumps(x).encode('utf-8'))



consumer = KafkaConsumer("error-test", group_id ='error-group',bootstrap_servers=['172.16.28.220:19092'],auto_offset_reset='earliest',
                         value_deserializer = lambda x: loads(x.decode('utf-8')), enable_auto_commit=True)



for i in range(3):
    data = {"{}".format(str(i)):
        "Hello {}".format(str(i))}
    
    producer.send("error-test",data)
    
    
print("producing done")

# for message in consumer:
#     if message is None:
#         print("consumer is waiting")
#         consumer.pause(1)
#     else:
#         print(message.value)
            
while True:            
    message = consumer.poll(1)
    consumer.task
    if message is {}:
        print("waiting for the message")
        time.sleep(1)
    
    else:
        for key,value in message.items():
            for i in value:
                print(i.value)
                