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

def json_reader(jsonname):
    with open(jsonname,'r') as f:
        json_data = json.load(f)
    return json_data


logger = logging.getLogger("log")
logger.setLevel(logging.INFO)
streamHandler = logging.StreamHandler()


formatter =logging.Formatter('%(asctime)s |%(name)s | %(levelname)s: %(message)s')

streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

fileHandler = logging.FileHandler("./test.log")
fileHandler.setLevel(logging.INFO)
fileHandler.setFormatter(formatter)

logger.addHandler(streamHandler)
logger.addHandler(fileHandler)





producer = KafkaProducer(acks=0,
                         compression_type = 'gzip',
                         bootstrap_servers=['172.16.28.218:19092','172.16.28.218:29092','172.16.28.218:39092','172.16.28.218:49092','172.16.28.218:59092'],
                         value_serializer= lambda x: dumps(x).encode('utf-8'))

 
os.getcwd()
# os.chdir("./")
os.getcwd()


json_value1 = json_reader("newtopicjson1093.json")
json_value2 = json_reader("newtopicjson1094.json")
json_value3 = json_reader("newtopicjson1095.json")


json_lst = [json_value1,json_value2,json_value3] 

# while True:
for i in range(1,len(json_lst)):
    start = time.time()
    data = json_lst[0]
    # print(data)
    producer.send("kalman-10-source",data)
    # producer.flush()
    # print('sent')
    time.sleep(1)
            # print("producing time :", time.time()- start)
            # logger.info("consumed time: {}".format(time.time()-start))
        
print("producing done")