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



os.getcwd()
os.chdir("/Users/e8l-20210032/Downloads/addXY_new3/")
os.getcwd()

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
        # if line[0] == '1903':
        # if line[0] == '1374': ######### 문제 해결 필요################
        current_car.append(line)
            
    f.close()
    
temp = 900
my_lst = []
producer = KafkaProducer(acks=0,
                         bootstrap_servers=['172.16.28.220:19092'],
                         compression_type='gzip',
                         value_serializer = lambda x: dumps(x).encode('utf-8'))

print("Producing Start")
produce_start = time.time()
for i in range(len(current_car)-1):
    #plt.scatter(float(current_car[i][5]),float(current_car[i][6]),c = 'r')
    # my_lst.append((float(current_car[i][5]),float(current_car[i][6])))
    
    
    # plt.scatter(float(current_car[i][5]),float(current_car[i][6]),c='b')
    data = {"key": current_car[i][0],
            "coordinates":
                [float(current_car[i][5]),
                 float(current_car[i][6])]
                }
    producer.send("batchkafka",data)

print("producing done: ",time.time()-produce_start)

consumer = KafkaConsumer("batchkafka",
                         bootstrap_servers=['172.16.28.220:19092'],
                         group_id="batchkafka-group",
                         auto_offset_reset="earliest",
                         enable_auto_commit=True,
                         value_deserializer= lambda x: loads(x.decode('utf-8')),
                         consumer_timeout_ms=1000
                         )


print("Kalman Start")
start = time.time()
my_lst2 = []

consumer_time = time.time()
    
for message in consumer:
    if message.value['id']:
        # xy_lst = [[float(current_car[i][5]),float(current_car[i][6])],[float(current_car[i][5])+2,float(current_car[i][6])+2]]
        
        current_map = {"{}".format(current_car[i][0]):  [float(current_car[i][5]),float(current_car[i][6])]}
        
        previous_map = {"{}".format(current_car[i][0]):  [float(current_car[i][5]),float(current_car[i][6])]}
        
consumer.close()

for key,value in lst_map.items():
    
    measurements = np.asarray(value)
        
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

    print(smoothed_state_means)
    
print("consuming done", time.time()-consumer_time)
    







################## 위에꺼 빼면 완료
# for i in range(len(current_car)-1):
#     xy_lst = [[float(current_car[i][5]),float(current_car[i][6])],[float(current_car[i][5])+2,float(current_car[i][6])+2]]
#     measurements = np.asarray(xy_lst)
        
#     initial_state_mean = [measurements[0, 0],
#                         0,
#                         measurements[0, 1],
#                         0]

#     transition_matrix = [[1, 1, 0, 0],
#                         [0, 1, 0, 0],
#                         [0, 0, 1, 1],
#                         [0, 0, 0, 1]]

#     observation_matrix = [[1, 0, 0, 0],
#                         [0, 0, 1, 0]]

#     kf1 = kf(transition_matrices = transition_matrix,
#                     observation_matrices = observation_matrix,
#                     initial_state_mean = initial_state_mean)


#     kf1 = kf1.em(measurements, n_iter=5)
#     (smoothed_state_means, smoothed_state_covariances) = kf1.smooth(measurements)
    
    
#     xy_lst = []

    
# print("Done time: ", time.time()- start)
# plt.show()