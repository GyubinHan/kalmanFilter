import numpy as np
import pandas as pd 
from pykalman import KalmanFilter as kf
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
import logging
from queue import Queue
from concurrent import futures
from multiprocessing import Process, Queue



transition_matrix = [[1, 1, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, 1],
                    [0, 0, 0, 1]]

observation_matrix = [[1, 0, 0, 0],
                    [0, 0, 1, 0]]

def kalmanfilter(value):
    lst_return = []
    # print(value)
    
    measurements = np.asarray(value)
    
    initial_state_mean = [measurements[0, 0],
                    0,
                    measurements[0, 1],
                    0]

    kf1 = kf(transition_matrices = transition_matrix,
                    observation_matrices = observation_matrix,
                    initial_state_mean = initial_state_mean)


    kf1 = kf1.em(measurements, n_iter=100)
    (smoothed_state_means, smoothed_state_covariances) = kf1.smooth(measurements)

    lst_return.append(smoothed_state_means)
    # dict = {dict_key:[lst_return]}
    # print(lst_return)
    return lst_return
    # return dict


def kalmanfilter2(value,kf2):
    lst_return = []
    # print(value)
    
    measurements = np.asarray(value)
    
    initial_state_mean = [measurements[0, 0],
                    0,
                    measurements[0, 1],
                    0]

    kf2.initial_state_mean = initial_state_mean
    
    kf2 = kf2.em(measurements, n_iter=3)
    (smoothed_state_means, smoothed_state_covariances) = kf2.smooth(measurements)

    lst_return.append(smoothed_state_means)
    # dict = {dict_key:[lst_return]}
    # print(lst_return)
    return lst_return
    # return dict

def json_reader(jsonname):
    with open(jsonname,'r') as f:
        json_data = json.load(f)
    return json_data


def jsonToDict(value):
    current_map = {
                '{}'.format(value[key_lst[0]]):
                {
                'linkId' : value[key_lst[1]],
                'lane' : value[key_lst[2]],
                'location' : value[key_lst[3]],
                'speed' : value[key_lst[4]],
                'position' : value[key_lst[5]],
                # 'destination' : value[key_lst[6]] ###### 실제 데이터에 사용
                }
            }
    return current_map


def DictToJson(key,value,kalman_lst,time):
    current_map = {
                
            "time": time,
             "vehicles": [
                 {
                'id':key,
                'linkId' : value[key_lst[1]],
                'lane' : value[key_lst[2]],
                'location' : value[key_lst[3]],
                'speed' : value[key_lst[4]],
                'position' : value[key_lst[5]],
                'kalman_position': [kalman_lst[0][len(kalman_lst[0])-1][0],kalman_lst[0][len(kalman_lst[0])-1][2]],
                # 'destination' : value[key_lst[6]] ###### 실제 데이터에 사용
                }]
    }
    return current_map


def DictToJsonAppend(key,value,kalman_lst):
    current_map = {
                'id':key,
                'linkId' : value[key_lst[1]],
                'lane' : value[key_lst[2]],
                'location' : value[key_lst[3]],
                'speed' : value[key_lst[4]],
                'position' : value[key_lst[5]],
                'kalman_position': [kalman_lst[0][len(kalman_lst[0])-1][0],kalman_lst[0][len(kalman_lst[0])-1][2]],
                # 'destination' : value[key_lst[6]] ###### 실제 데이터에 사용
                }
    
    return current_map

def json_reader(jsonname):

    with open(jsonname,'r') as f:

        json_data = json.load(f)

    return json_data

def work(input_lst, results):
    for input in input_lst:
        results.put(kalmanfilter(input))
    return

def list_chuck(arr, n):
    return [arr[i: i + n] for i in range(0, len(arr), n)]

def multi_kalman(vehicles_lst):
    results = Queue()
    partOf_lst = list_chuck(vehicle_lst, 3)
    ps1 = Process(target=work, args=(partOf_lst[0], results))
    ps2 = Process(target=work, args=(partOf_lst[1], results))
    ps3 = Process(target=work, args=(partOf_lst[2], results))
    ps1.start()
    ps2.start()
    ps3.start()
    ps1.join()
    ps2.join()
    ps3.join()
    

## release
# producer = KafkaProducer(acks=0,
#                          compression_type = 'gzip',
#                          bootstrap_servers=['172.16.28.218:19092','172.16.28.218:29092','172.16.28.218:39092','172.16.28.218:49092','172.16.28.218:59092'],
#                          value_serializer= lambda x: dumps(x).encode('utf-8'))



# consumer = KafkaConsumer("dev.pintel.simul.withLocation.vehicle.json", group_id ='ndxpro.pintel.group',bootstrap_servers=['172.16.28.218:19092','172.16.28.218:29092','172.16.28.218:39092','172.16.28.218:49092','172.16.28.218:59092'],auto_offset_reset='earliest',
#                          value_deserializer = lambda x: loads(x.decode('utf-8')), enable_auto_commit=True)

# producer = KafkaProducer(acks=0,
#                          compression_type = 'gzip',
#                          bootstrap_servers=['172.16.28.220:19092'],
#                          value_serializer= lambda x: dumps(x).encode('utf-8'))
# consumer = KafkaConsumer("kk-receiver2", group_id ='ndxpro.pintel.group',bootstrap_servers=['172.16.28.220:19092'],auto_offset_reset='earliest',
#                          value_deserializer = lambda x: loads(x.decode('utf-8')), enable_auto_commit=False)

# ##### test version
# producer = KafkaProducer(acks=0,
#                          compression_type = 'gzip',
#                          bootstrap_servers=['172.16.28.220:19092'],
#                          value_serializer= lambda x: dumps(x).encode('utf-8'))



# consumer = KafkaConsumer("kk-receiver2", group_id ='ndxpro.pintel.group',bootstrap_servers=['172.16.28.220:19092']
#                          ,auto_offset_reset='earliest',
#                          value_deserializer = lambda x: loads(x.decode('utf-8')), enable_auto_commit=True, max_poll_interval_ms = 900000,
#                          auto_commit_interval_ms=500)

if __name__ == "__main__":

    log = logging.getLogger(__name__)

    temp = 0 
    interval = 1
    print("Hello,it is starting")


    start = time.time()

    topic = 'kk-sender2'

    que = Queue()

    kf2 = kf(transition_matrices = transition_matrix,
                    observation_matrices = observation_matrix)
  

    json_lst = []
    for i in range(1093, 1100):
        json_lst.append(json_reader("newtopicjson" + i.__str__() + ".json"))



    for message in json_lst:
        messageLength = len(message['vehicles'])
        if  messageLength == 0 :
            print('no Data')
            print(que.get())
            break

        start = time.time()
        
        try:
            key_lst = list(message['vehicles'][0].keys())
            
            current_map = jsonToDict(message['vehicles'][0])
            for i in range(1, messageLength) :
                current_map.update(jsonToDict(message['vehicles'][i]))
            # queue 생성 
            # queSize = que.qsize()
            # if queSize == 3 :
            #     que.get()
            # que.put(current_map)

            #### previous_map copy
            if temp == 0:
                previous_map = copy.deepcopy(current_map)
                new_lst = []
                dataBool = False
                print('before kalman = ', time.time() - start)
                vehicle_lst = []
                for value in current_map:
                    previous_map[value]['position'].clear()
                    previous_map[value]['position'].append([current_map[value]['position'][0]-1,current_map[value]['position'][1]-1])
                    new_lst = previous_map[value]['position'][:] # previous_map과 주소값을 다르게 하기 위해 slicing
                    new_lst.append([current_map[value]['position'][0],current_map[value]['position'][1]])
                    vehicle_lst.append(new_lst)
                    # kalman_lst = kalmanfilter(new_lst)

                multi_kalman(vehicle_lst)

                print('after kalnam = ', time.time() - start)
                temp += 1
                current_map = {}
                print("consumer time", time.time()-start)

            else:
                dataBool = False
                print('before kalman = ', time.time() - start)
                for value in current_map:
                    previous_map_keys = previous_map.keys()
                    current_map_keys = current_map.keys()

                    ########## current map과 previous map 다른 키
                    diff = set(current_map)-set(previous_map)
                    if diff:
                        new_lst = []
                        for i in diff:
                            temp_copy = copy.deepcopy({i:current_map[i]}) ## 주소값 변경
                            previous_map.update(temp_copy)
                            previous_map[i]['position'].clear()
                            previous_map[i]['position'].append([current_map[i]['position'][0]-1,current_map[i]['position'][1]-1])
                            new_lst = previous_map[i]['position'][:]
                            new_lst.append([current_map[i]['position'][0],current_map[i]['position'][1]])
                            kalman_lst = kalmanfilter(new_lst)
                            
                    ########## current map과 previous map 같은 키
                    else:
                        new_lst = []
                        new_lst = previous_map[value]['position'][:]
                        previous_map[value]['position'].pop(0)
                        previous_map[value]['position'].append([current_map[value]['position'][0],current_map[value]['position'][1]]) 
                        new_lst.append([current_map[value]['position'][0],current_map[value]['position'][1]])
                        kalman_lst = kalmanfilter(new_lst)

                print('after kalnam = ', time.time() - start)
                current_map = {}
                print("consumer time", time.time()-start)
                
                
        except KafkaError as e:
            log.exception("Problem communicating with Kafka, retrying in %d seconds...", interval)

            print(message.error)



