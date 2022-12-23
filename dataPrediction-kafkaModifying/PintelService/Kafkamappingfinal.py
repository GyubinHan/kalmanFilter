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


def kalmanfilter(value):
    lst_return = []
    # print(value)
    
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
    # dict = {dict_key:[lst_return]}
    # print(lst_return)
    return lst_return
    # return dict

def json_reader(jsonname):
    with open(jsonname,'r') as f:
        json_data = json.load(f)
    return json_data
 
def Convert(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct

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

def jsonToDictUpdate(current_map,value):
    
    current_map.update({
                '{}'.format(value[key_lst[0]]):
                {
                'linkId' : value[key_lst[1]],
                'lane' : value[key_lst[2]],
                'location' : value[key_lst[3]],
                'speed' : value[key_lst[4]],
                'position' : value[key_lst[5]],
                # 'destination' : value[key_lst[6]] ###### 실제 데이터에 사용
                
                }
            })
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

os.getcwd()
os.chdir("KafkaKalman/")
os.getcwd()



json_value1 = json_reader("newtopicjson1.json")
json_value2 = json_reader("newtopicjson2.json")
json_value3 = json_reader("newtopicjson3.json")


os.chdir("../PintelService/")


logging.basicConfig(
            format='%(asctime)s %(levelname)s %(message)s', 
            level=logging.INFO, 
            datefmt='%m/%d/%Y %I:%M:%S %p'
            )
logger = logging.getLogger('ndxpro-pintel-kalman')


formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)

f1 = logging.FileHandler(filename = "./dataPrediction.log")
f1.setLevel(logging.INFO)
f1.setFormatter(formatter)
logger.addHandler(f1)


logger.setLevel(level=logging.INFO)






key_lst = list(json_value1['vehicles'][0].keys())
# print(key_lst)

json_lst = [json_value1,json_value2,json_value3] 

previous_map = {}

count = 0 
interval = 0

topic = 'kk-sender2'

producer = KafkaProducer(acks=1,
                         bootstrap_servers=['172.15.2.3:9000'],
                         compression_type='gzip',
                         value_serializer=lambda x: dumps(x.encode('utf-8')))
for j in range(len(json_lst)):
    start = time.time()
    logger.info(f"time: {j} consume: {time.time()-start}")
    
    try:
        for i in range(len(json_lst[j]['vehicles'])):
            
            # json to dictionary(hashmap)    
            if i == 0 :
                current_map = jsonToDict(json_lst[j]['vehicles'][i])
                # print("test1")
            else:
                current_map.update(jsonToDict(json_lst[j]['vehicles'][i]))
                # print("test2")
                
            
            #### previous_map copy
        if j == 0:
                previous_map = copy.deepcopy(current_map)
                new_lst = []
                dataBool = False
                for value in current_map:
                    # print(type(previous_map[value]['position']))
                    previous_map[value]['position'].clear()
                    previous_map[value]['position'].append([current_map[value]['position'][0]-1,current_map[value]['position'][1]-1])
                    
                    new_lst = previous_map[value]['position'][:] # previous_map과 주소값을 다르게 하기 위해 slicing
                    # new_lst.append(current_map[value]['position'])
                    
                    new_lst.append([current_map[value]['position'][0],current_map[value]['position'][1]])
                    # print(new_lst)
                    kalman_lst = kalmanfilter(new_lst)
                    # print(kalman_lst)
                
                    data = DictToJson(value,current_map[value],kalman_lst,j)
                    
                    if dataBool:
                        data['vehicles'].append(DictToJsonAppend(value,current_map[value],kalman_lst))
                    else:
                        data = DictToJson(value,current_map[value],kalman_lst,j)
                        dataBool = True
                    # print(value)
                    # print(data)
                producer.send(topic,data)
                # temp += 1
                current_map = {}
                logger.info(f"info: {j} {time.time()-start}")
                print("consumer time", time.time()-start)
        else:
                dataBool = False
                
                for value in current_map:
                    previous_map_keys = previous_map.keys()
                    current_map_keys = current_map.keys()

                    # print("test4")

                    ########## current map과 previous map 다른 키
                    diff = set(current_map)-set(previous_map)
                
                    # if (current_map_keys!=previous_map_keys):
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
                            # print(kalman_lst)

                        # print(kalman_lst[0][len(kalman_lst[0])-1][0],kalman_lst[0][len(kalman_lst[0])-1][2]) # final kalman filter coordinates
                        
                        
                            if dataBool:
                                data['vehicles'].append(DictToJsonAppend(value,current_map[value],kalman_lst))
                            else:
                                data = DictToJson(value,current_map[value],kalman_lst,j)
                                dataBool = True
                            # print(data)
                            # producer.send("kk-sender2",data)

                            
                    ########## current map과 previous map 같은 키
                    else:
                        
                        new_lst = []
                        new_lst = previous_map[value]['position'][:]
                        previous_map[value]['position'].pop(0)
                        previous_map[value]['position'].append([current_map[value]['position'][0],current_map[value]['position'][1]]) 
                        new_lst.append([current_map[value]['position'][0],current_map[value]['position'][1]])
                        
                        # print(new_lst) 
                        kalman_lst = kalmanfilter(new_lst)
                        # print(kalman_lst)
                        
                        if dataBool:
                            data['vehicles'].append(DictToJsonAppend(value,current_map[value],kalman_lst))
                        else:
                            data = DictToJson(value,current_map[value],kalman_lst,j)
                            dataBool = True

                producer.send(topic,data)
                # producer.send(test_topic,data)
                
                # temp += 1
                current_map = {}
                logger.info(f"info: {j} {time.time()-start}")
                print("consumer time", time.time()-start)
                
    except KafkaError as e:
        logger.exception("Problem communicating with Kafka, retrying in %d seconds...", interval)

        print(f"kafka error: {e}")

print("Done")
    # print(previous_map[value]['position'][0],previous_map[value]['position'][1])
    # print(kalman_lst[0][0][0],kalman_lst[0][0][2]) # 써야하는 좌표
    # print(kalman_lst[0][1][0],kalman_lst[0][1][2]) # 예비 좌표
    # print(kalman_lst)