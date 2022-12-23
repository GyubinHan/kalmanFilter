from kafka import KafkaProducer
from kafka import KafkaConsumer
from json import loads, dumps
import numpy as np
import pandas as pd
import requests
import json
from pykalman import KalmanFilter as kf
import matplotlib.pyplot as plt


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


x1 = '-5747872.696975'
x2 = '-5747817.747455'
y1 = '-967926.685685'
y2 = '-967895.899235'

plt.scatter(x1,y1,c='b')
plt.scatter(x2,y2,c='b')


data = {"key1": '650',
        "coordinates":[
            x1,
            y1
            
        ]
        }


data2 = {"key2": '652',
        "coordinates":[
            x2,
            y2
            
        ]
        }



# producer.send('kalmanfilter-1',)

producer.send("kalmanfilter-1",data)
producer.send("kalmanfilter-1",data2)
print("producing done")


consumer = KafkaConsumer("kalmanfilter-1",
                         group_id = "kalman-test1",
                         bootstrap_servers=['172.16.28.220:19092'],
                         value_deserializer= lambda x: loads(x.decode('utf-8')),
                         auto_offset_reset ='earliest',
                         enable_auto_commit=True)

my_lst = [[float(x1)-1,float(y1)-1]]

for message in consumer:
    #print(message.value)
    # print(my_lst)
    
    my_lst.append([float(message.value['coordinates'][0]),float(message.value['coordinates'][1])])
    k = kalmanfilter(my_lst)
   
    print(k[0][0][0],k[0][0][2])
    print(k[0][1][0],k[0][1][2])
    
    plt.scatter(k[0][0][0],k[0][0][2],c='r')
    plt.scatter(k[0][1][0],k[0][1][2],c='r')
    # print(type(k[0][1][0]),type(k[0][1][2]))
        
    # # print(k[0][0])
    # else:
    #     plt.scatter(float(k[0][0][0]),float(k[0][0][2]),c='r')
    #     plt.scatter(float(k[0][1][0]),float(k[0][1][2]),c='r')
    print(my_lst)
    del my_lst[0]
    # plt.show()    
