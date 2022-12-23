from kafka import KafkaProducer
from kafka import KafkaConsumer
from json import loads, dumps
import numpy as np
import pandas as pd
import requests
import json
from pykalman import KalmanFilter as kf
import matplotlib.pyplot as plt
import csv
import os
import time

def kalmanfilter(lst):
    new_lst = []
    measurements = np.asarray(lst)
    
    initial_state_mean = [measurements[0, 0],
                        0,
                        measurements[0, 1],
                        0]


    transition_matrix = [[1, 1, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 1, 1],
                        [0, 0, 0, 1]]

    observation_matrix = [[1, 0, 0, 0],
                        [0, 0, 1, 0]]

    kf1 = kf(transition_matrices = transition_matrix,
                    observation_matrices = observation_matrix,
                    initial_state_mean = initial_state_mean)
    kf1 = kf1.em(measurements, n_iter=5)
    (smoothed_state_means, smoothed_state_covariances) = kf1.smooth(measurements)
    new_lst.append(smoothed_state_means)
    return new_lst



producer = KafkaProducer(acks=0,
                         bootstrap_servers=['172.16.28.220:19092'],
                         compression_type='gzip',
                         value_serializer= lambda x: dumps(x).encode('utf-8')
                         )


os.getcwd()
os.chdir("/Users/e8l-20210032/Downloads/addXY_new3/")
os.getcwd()
start = time.time()
path = "Vehicle_Info__VISSIM_Time_"
file_format = ".csv"
csv_lst = []
for i in range(900,901):
    s = path+str(i)+file_format
    csv_lst.append(s)

current_car = []  
for c in csv_lst:
    f = open(c, 'r', encoding='utf-8' )     
    rdr = csv.reader(f)
    for line in rdr:
        #print(type(line[0])) # str
        # if line[0] == '1374':
        # if line[0] == '672': ######### 문제 해결 필요################
        current_car.append(line)
        
            
f.close()


# print("start time: ",start)
# for i in range(len(current_car)):
#     data = {"id":"{}".format(current_car[i][0]),
#              "coordinates":[
#             current_car[i][5],
#             current_car[i][6]
            
#         ]
#             }
#     producer.send("time-check-kafka",data)

# print("Producing done!")
# print("Producing time", time.time()-start)

consumer = KafkaConsumer("kk-receiver2",
                         bootstrap_servers=["172.16.28.220:19092"],
                         group_id = "kk-group2",
                         auto_offset_reset='earliest',
                         enable_auto_commit=True,
                         value_deserializer= lambda x : loads(x.decode('utf-8')), 
                        # consumer_timeout_ms = 1500
                         )

new_start = 0 
my_lst = []
start2 = time.time()
print("Before Consume : ", start2)


for message in consumer:
    # print(message.value)
    start = time.time()
    
    for val in message.value['vehicles']:
        my_lst.append([val['position'][0]-1,val['position'][1]-1])
        my_lst.append([val['position'][0],val['position'][1]])
        k = kalmanfilter(my_lst)
        my_lst = []    
    
        
    
    
    # print(message.value)
    
    # print("After kalman filter: ", time.time()-kalman_time)
    # print(k)
    # producing_time = time.time()
    # producer.send("time-check-kafka-end",data)
    print("send time :",time.time()-start)
    
    # print("After Producing: ", time.time()-producing_time)
# producer.flush()
    
print("Consuming done!")
print("Consuming time", time.time()-start2)

