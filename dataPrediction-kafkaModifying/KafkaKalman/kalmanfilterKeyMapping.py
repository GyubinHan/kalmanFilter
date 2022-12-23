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

def map_update(json_value):
    # previous_map = {}
    # if previous_map:
    previous_map.update({
        '{}'.format(json_value[key_lst[0]]):
        {
        'linkId' : json_value[key_lst[1]],
        'lane' : json_value[key_lst[2]],
        'location' : json_value[key_lst[3]],
        'speed' : json_value[key_lst[4]],
        'position' : json_value[key_lst[5]],
        }
    })
    # else:
        
    #     previous_map = {
    #         '{}'.format(value[key_lst[0]]):
    #         {
    #         'linkId' : value[key_lst[1]],
    #         'lane' : value[key_lst[2]],
    #         'location' : value[key_lst[3]],
    #         'speed' : value[key_lst[4]],
    #         'position' : value[key_lst[5]],
    #         }
    #     }
    return previous_map

def kalmanfilter(value):
    lst_return = []
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

    lst_return.append(smoothed_state_means)
    return lst_return

def json_reader(jsonname):
    with open(jsonname,'r') as f:
        json_data = json.load(f)
    return json_data
 
 
 
def Convert(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct

os.getcwd()
os.chdir("KafkaKalman/")
os.getcwd()



json_value1 = json_reader("topicjson1.json")


key =[key for key in json_value1]
# print(key)

key_lst = list(json_value1[0].keys())



current_map = {}
previous_map = {}
for value in json_value1:
    # print(value[key_lst[0]]) key number
    # print(value)
    # previous_map = map_update(value)
    if previous_map:
        previous_map.update({
            '{}'.format(value[key_lst[0]]):
            {
            'linkId' : value[key_lst[1]],
            'lane' : value[key_lst[2]],
            'location' : value[key_lst[3]],
            'speed' : value[key_lst[4]],
            'position' : value[key_lst[5]],
            }
        })
    else:
        
        previous_map = {
            '{}'.format(value[key_lst[0]]):
            {
            'linkId' : value[key_lst[1]],
            'lane' : value[key_lst[2]],
            'location' : value[key_lst[3]],
            'speed' : value[key_lst[4]],
            'position' : value[key_lst[5]],
            }
        }

# print(type(previous_map['963']['position'][0]))
new_lst = []
for value in previous_map:
    new_lst = [[previous_map[value]['position'][0]-1,previous_map[value]['position'][1]-1],[previous_map[value]['position'][0],previous_map[value]['position'][1]]]
    kalman_lst = kalmanfilter(new_lst)
    # print(value,'  ',previous_map[value]['position'])
    # print('kalman predicted', new_lst)
    # print(kalman_lst)
    # if value == '1763':
        # plt.scatter(previous_map[value]['position'][0],previous_map[value]['position'][1],c='b')
        # plt.scatter(kalman_lst[0][1][0],kalman_lst[0][1][2],c='r')
    print(previous_map[value]['position'][0],previous_map[value]['position'][1])
    # print(kalman_lst[0][0][0],kalman_lst[0][0][2]) # 써야하는 좌표
    # print(kalman_lst[0][1][0],kalman_lst[0][1][2]) # 예비 좌표
    print(kalman_lst)
# plt.show()
# json_value3 = json_reader("topicjson3.json")
# print(type(json_value1))
# json_convert = Convert(json_value1)
# dict = {json_value1[i]: json_value1[i + 1] for i in range(0, len(json_value1), 2)}

# print(type(dict))

# for key,value 
# in json_value1:
#     print(key)



# for i in json_value1:
#     print(i.key())