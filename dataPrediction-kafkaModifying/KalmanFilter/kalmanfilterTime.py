from kafka import KafkaProducer
from kafka import KafkaConsumer
from json import loads, dumps
import numpy as np
import pandas as pd
# import requests
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
    kf1 = kf1.em(measurements, n_iter=1)
    (smoothed_state_means, smoothed_state_covariances) = kf1.smooth(measurements)
    new_lst.append(smoothed_state_means)
    return new_lst

def kalmanfilter2(lst):
    new_lst = []
    measurements = np.asarray(lst)
    kf2 = kf(transition_matrices = [[1, 1], [0, 1]], observation_matrices = [[0.1, 0.5], [-0.3, 0.0]])
    kf2 = kf2.em(measurements, n_iter=5)
    (filtered_state_means, filtered_state_covariances) = kf2.filter(measurements)
    (smoothed_state_means, smoothed_state_covariances) = kf2.smooth(measurements)
    return new_lst

def kalmanfilter3(lst):
    new_lst = []
    n_real_time = 3
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
    
    kf3 = kf(transition_matrices = transition_matrix,
                    observation_matrices = observation_matrix,
                    initial_state_mean = initial_state_mean,
                    # observation_covariance = 10* kf3.observation_covariance,
                    em_vars=['transition_covariance', 'initial_state_covariance'])

    kf3 = kf3.em(measurements, n_iter=5)
    (filtered_state_means, filtered_state_covariances) = kf3.filter(measurements)
    
    
    return new_lst


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
print(current_car[0])

# start = time.time()
lst = [[0,0]]
print("Start")
for i in range(len(current_car)):
    start = time.time()
    lst = [[float(current_car[i][5])-1,float(current_car[i][6])-1],[float(current_car[i][5]),float(current_car[i][6])]]
    k = kalmanfilter(lst)
    # k2 = kalmanfilter2(lst)
    # k3 = kalmanfilter3(lst)
    print(time.time()-start)

# print("kalman done",time.time()-start)
    