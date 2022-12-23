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
from logging import StreamHandler



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

    kf1 = kf1.em(measurements, n_iter=1)
    (smoothed_state_means, smoothed_state_covariances) = kf1.smooth(measurements)

    lst_return.append(smoothed_state_means)
 
    return lst_return

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


sourceTopic = os.environ['SOURCE_TOPIC']

targetTopic = os.environ['TARGET_TOPIC']

kafka_url = os.environ['KAFKA_URL'].split(',')

consumer_group = os.environ['CONSUMER_GROUP']

kalman_number = os.environ['KALMAN_NUMBER']

kalman_log = os.environ['KALMAN_LOG']

## release
# sourceTopic = "docker10-source"
# targetTopic = "docker10-target"
# kafka_url = ['localhost:19092']
# consumer_group = 'kalman.group.0'
# kalman_number = 0

# producer = KafkaProducer(acks=0,
#                          compression_type = 'gzip',
#                          bootstrap_servers=['172.16.28.192.218:19092'],
#                          value_serializer= lambda x: dumps(x).encode('utf-8'))


# # consume_topic = 'dev.pintel.simul.withLocation.vehicle.json'
# consumer = KafkaConsumer(sourceTopic, group_id =consumer_group,
#                          bootstrap_servers=kafka_url,
#                          auto_offset_reset='earliest',
#                          value_deserializer = lambda x: loads(x.decode('utf-8')),enable_auto_commit=True)




##### test version
producer = KafkaProducer(acks=0,
                         compression_type = 'gzip',
                         bootstrap_servers=kafka_url,
                         value_serializer= lambda x: dumps(x).encode('utf-8'))



consumer = KafkaConsumer(sourceTopic, group_id =consumer_group,bootstrap_servers=kafka_url
                         ,auto_offset_reset='earliest',
                         value_deserializer = lambda x: loads(x.decode('utf-8')), enable_auto_commit=True, max_poll_interval_ms = 900000,
                         auto_commit_interval_ms=500)





logger = logging.getLogger('ndxpro-pintel-kalman')
logging.basicConfig(
            format='%(asctime)s %(levelname)s %(message)s', 
            level=logging.INFO, 
            datefmt='%m/%d/%Y %I:%M:%S %p'
            )
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)

f1 = logging.FileHandler(f"/app/logFile/{kalman_log}")

f1.setLevel(logging.INFO)
f1.setFormatter(formatter)
logger.addHandler(f1)


# f2 = logging.FileHandler("/mnt/hdd1/usr/root/logs/data-prediction/dataPredictionERROR.log")
# f2.setLevel(logging.ERROR)
# f2.setFormatter(formatter)
# logger.addHandler(f2)


# current_map = {}
temp = 0 
interval = 0
print("Data-prediction starts")
# topic = 'dev.pintel.simul.withKalman.vehicle.json'


for message in consumer:
    start = time.time()
    try:
        key_lst = list(message.value['vehicles'][0].keys())
        current_map = {}
        for i in range(len(message.value['vehicles'])):
            
            if message.value['vehicles'][i][key_lst[0]]%10 == kalman_number:
                # logger.info(f"Time(frame): {message.value['time']}, Vehicle No: {message.value['vehicles'][i]}")
                # json to dictionary(hashmap)    
                if i == 0 :
                    current_map = jsonToDict(message.value['vehicles'][i])
                else:
                    current_map.update(jsonToDict(message.value['vehicles'][i]))
                
        #### previous_map copy
        if temp == 0:
            previous_map = copy.deepcopy(current_map)
            new_lst = []
            dataBool = False
            for value in current_map:
                # if value%10 == kalman_number:
                    # logger.info(f"Time(frame): {message.value['time']}, Vehicle No: {message.value['vehicles'][i]}, start-time: {time.time()}")
                    
                    previous_map[value]['position'].clear()
                    previous_map[value]['position'].append([current_map[value]['position'][0]-1,current_map[value]['position'][1]-1])
                    
                    new_lst = previous_map[value]['position'][:] # previous_map과 주소값을 다르게 하기 위해 slicing
                    
                    new_lst.append([current_map[value]['position'][0],current_map[value]['position'][1]])
                    kalman_lst = kalmanfilter(new_lst)
                
                    data = DictToJson(value,current_map[value],kalman_lst,message.value['time'])
                    
                    if dataBool:
                        data['vehicles'].append(DictToJsonAppend(value,current_map[value],kalman_lst))
                    else:
                        data = DictToJson(value,current_map[value],kalman_lst,message.value['time'])
                        dataBool = True

            producer.send(targetTopic,data)
            temp += 1
            current_map = {}
            # logger.info(f"Source Topic:{sourceTopic},  Target Topic: {targetTopic},  Time(frame): {message.value['time']},  Consuming time: {time.time()-start}")
        else:
            dataBool = False
            
            for value in current_map:
                previous_map_keys = previous_map.keys()
                current_map_keys = current_map.keys()

                ########## current map과 previous map 다른 키
                # if value%10 == kalman_number:
                    # logger.info(f"Time(frame): {message.value['time']}, Vehicle No: {message.value['vehicles'][i]}, start-time: {time.time()}")
                start = time.time()
            
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

                    # print(kalman_lst[0][len(kalman_lst[0])-1][0],kalman_lst[0][len(kalman_lst[0])-1][2]) # final kalman filter coordinates
                    
                    
                        if dataBool:
                            data['vehicles'].append(DictToJsonAppend(value,current_map[value],kalman_lst))
                        else:
                            data = DictToJson(value,current_map[value],kalman_lst,message.value['time'])
                            dataBool = True

                        
                ########## current map과 previous map 같은 키
                else:
                    
                    new_lst = []
                    new_lst = previous_map[value]['position'][:]
                    previous_map[value]['position'].pop(0)
                    previous_map[value]['position'].append([current_map[value]['position'][0],current_map[value]['position'][1]]) 
                    new_lst.append([current_map[value]['position'][0],current_map[value]['position'][1]])
                    
                    kalman_lst = kalmanfilter(new_lst)
                    
                    if dataBool:
                        data['vehicles'].append(DictToJsonAppend(value,current_map[value],kalman_lst))
                    else:
                        data = DictToJson(value,current_map[value],kalman_lst,message.value['time'])
                        dataBool = True
                # else: continue

            producer.send(targetTopic,data)
            
            # temp += 1
            current_map = {}
        logger.info(f"{message} \n Source Topic:{sourceTopic},  Target Topic: {targetTopic},  Time(frame): {message.value['time']},  Consuming time: {time.time()-start}")
            
    except KafkaError as e:
        logger.exception("Problem communicating with Kafka, retrying in %d seconds...", interval)
        logger.error(f"{e} Source Topic: {sourceTopic}, Time: {message.value['time']}, Target Topic: {targetTopic}")
        print(message.error)



