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
                'destination' : value[key_lst[6]] ###### 실제 데이터에 사용
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
                'destination' : value[key_lst[6]] ###### 실제 데이터에 사용
                
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
                'destination' : value[key_lst[6]] ###### 실제 데이터에 사용
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
                'destination' : value[key_lst[6]] ###### 실제 데이터에 사용
                }
    
    return current_map


# sourceTopic = os.environ['SOURCE_TOPIC']

# targetTopic = os.environ['TARGET_TOPIC']

# kafka_url = os.environ['KAFKA_URL'].split(',')

# consumer_group = os.environ['CONSUMER_GROUP']

# kalman_number = os.environ['KALMAN_NUMBER']

# kalman_log = os.environ['KALMAN_LOG']





# ##test
sourceTopic =  'kalman-10-source'
targetTopic =  'kalman-10-target'
kafka_url =  ['172.16.28.218:19092','172.16.28.218:29092','172.16.28.218:39092','172.16.28.218:49092','172.16.28.218:59092']
# print(type(kafka_url))
# print(url.split(','))
consumer_group =  'kafka-5'
kalman_number =  5
kalman_log = 'kalmanlog5.log'



# ####### yaml working well
# import yaml

# with open('docker-compose.yml') as f:
#     yml = yaml.load(f, Loader=yaml.FullLoader)
    
    
    
# print(yml['services']['data-prediction0']['environment']['TARGET_TOPIC'])
# print(yml['services']['data-prediction0']['environment']['KAFKA_URL'].split(','))

# print(yml['services']['data-prediction0']['environment']['CONSUMER_GROUP'])
# print(yml['services']['data-prediction0']['environment']['KALMAN_NUMBER'])
# print(yml['services']['data-prediction0']['environment']['KALMAN_LOG'])



# sourceTopic = yml['services']['data-prediction0']['environment']['SOURCE_TOPIC']

# targetTopic = yml['services']['data-prediction0']['environment']['TARGET_TOPIC']

# kafka_url = yml['services']['data-prediction0']['environment']['KAFKA_URL'].split(',')

# consumer_group = yml['services']['data-prediction0']['environment']['CONSUMER_GROUP']

# kalman_number = yml['services']['data-prediction0']['environment']['KALMAN_NUMBER']

# kalman_log = 'kalmanlog0.log'



##### test version
producer = KafkaProducer(acks=0,
                         compression_type = 'gzip',
                         bootstrap_servers=kafka_url,
                         value_serializer= lambda x: dumps(x).encode('utf-8'))



consumer = KafkaConsumer(sourceTopic, group_id =consumer_group,bootstrap_servers=kafka_url
                         ,auto_offset_reset='earliest',
                         value_deserializer = lambda x: loads(x.decode('utf-8')), enable_auto_commit=True, max_poll_interval_ms = 3000000,
                         auto_commit_interval_ms=5000,heartbeat_interval_ms=30000, session_timeout_ms=100000)





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

f1 = logging.FileHandler(filename = kalman_log)
f1.setLevel(logging.INFO)
f1.setFormatter(formatter)
logger.addHandler(f1)


logger.setLevel(level=logging.INFO)





previous_map = {}
# current_map = {}
count = 0 
interval = 0

# topic = 'kk-sender2'
temp = 0
current_map = {}
for message in consumer:
    start = time.time()
    # logger.info(f"time: {j} consume: {time.time()-start}")
    key_lst = list(message.value['vehicles'][0].keys())
    try:
        for i in range(len(message.value['vehicles'])):
            # print(message.value['vehicles'][i][key_lst[0]]%10)
            if message.value['vehicles'][i][key_lst[0]]%10 == kalman_number:
                # json to dictionary(hashmap)    

                    current_map.update(jsonToDict(message.value['vehicles'][i]))
                        # print("test2")
                        
            
            #### previous_map copy
        if temp == 0:
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
                
                    # data = DictToJson(value,current_map[value],kalman_lst,message.value['time'])
                    if dataBool:
                        data['vehicles'].append(DictToJsonAppend(value,current_map[value],kalman_lst))
                    else:
                        data = DictToJson(value,current_map[value],kalman_lst,message.value['time'])
                        dataBool = True
                        
                    # print(value)
                    # print(data)
                print(data)
                # producer.send(targetTopic,data)
                temp += 1
                current_map = {}
                logger.info(f"Source Topic:{sourceTopic},  Target Topic: {targetTopic},  Time(frame): {message.value['time']},  Consuming time: {time.time()-start}")
                # print("consumer time", time.time()-start)
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
                                data = DictToJson(value,current_map[value],kalman_lst,message.value['time'])
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
                            data = DictToJson(value,current_map[value],kalman_lst,message.value['time'])
                            dataBool = True

                # producer.send(targetTopic,data)
                # producer.send(test_topic,data)
                
                # temp += 1
                print(data)
                
                current_map = {}
                logger.info(f"Source Topic:{sourceTopic},  Target Topic: {targetTopic},  Time(frame): {message.value['time']},  Consuming time: {time.time()-start}")
                # print("consumer time", time.time()-start)
                
                
    except KafkaError as e:
        logger.exception("Problem communicating with Kafka, retrying in %d seconds...", interval)

        print(f"kafka error: {e}")

print("Done")
    # print(previous_map[value]['position'][0],previous_map[value]['position'][1])
    # print(kalman_lst[0][0][0],kalman_lst[0][0][2]) # 써야하는 좌표
    # print(kalman_lst[0][1][0],kalman_lst[0][1][2]) # 예비 좌표
    # print(kalman_lst)ka