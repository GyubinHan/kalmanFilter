import json
import csv
import os
import numpy as np
from pykalman import KalmanFilter as kf
from queue import PriorityQueue
import threading

# que.put(json_value1)
# que.put(json_value2)
# print(que.get()['vehicles']['id'])
# print(que.get())




# current_map = {}
# previous_map = {}
# # print(json_value1)
# key_lst = list(json_value1['vehicles'][0].keys()) # key list

# previous_map = parse_dict(json_value1,key_lst) # dictionary 변환 
# current_map = parse_dict(json_value2,key_lst) # dictionary 변환 

# previous_map_keys = previous_map.keys()
# current_map_keys = current_map.keys()




# ########## current map과 previous map 다른 키
# if (current_map_keys!=previous_map_keys):
#     if (set(current_map)-set(previous_map)) in current_map:
#         print(set(current_map)-set(previous_map))
#     elif set(current_map)-set(previous_map) in previous_map['vehicles'].keys():
#         del(previous_map['vehicles'][set(current_map)-set(previous_map)])
#         print("deleted")
# # for key,value in dict.items():
    








# for value in range(len(json_value1['vehicles'])):
   
#     if previous_map:
#         previous_map = current_map.keys().deepcopy()
#     else:
#         previous_map = {
#                 '{}'.format(value[key_lst[0]]):
#                 {
#                 'linkId' : value[key_lst[1]],
#                 'lane' : value[key_lst[2]],
#                 'location' : value[key_lst[3]],
#                 'speed' : value[key_lst[4]],
#                 'position' : value[key_lst[5]],
#                 }
#             }
#     if current_map:
#         current_map.update({
#             '{}'.format(value[key_lst[0]]):
#             {
#             'linkId' : value[key_lst[1]],
#             'lane' : value[key_lst[2]],
#             'location' : value[key_lst[3]],
#             'speed' : value[key_lst[4]],
#             'position' : value[key_lst[5]],
#             }
#         })
#     else:
#         current_map = {
#                 '{}'.format(value[key_lst[0]]):
#                 {
#                 'linkId' : value[key_lst[1]],
#                 'lane' : value[key_lst[2]],
#                 'location' : value[key_lst[3]],
#                 'speed' : value[key_lst[4]],
#                 'position' : value[key_lst[5]],
#                 }
#             }


    # previous_map = map_update(value)