import numpy as np
import pandas as pd
from pykalman import KalmanFilter as kf
import os
import csv
import matplotlib.pyplot as plt
import time



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
for i in range(len(current_car)-1):
    #plt.scatter(float(current_car[i][5]),float(current_car[i][6]),c = 'r')
    my_lst.append((float(current_car[i][5]),float(current_car[i][6])))
    plt.scatter(float(current_car[i][5]),float(current_car[i][6]),c='b')

print("Start")
start = time.time()
# print(my_lst)
# print(my_lst)
my_lst2 = []
for i in range(len(current_car)-1):
    # my_lst2 = [[float(current_car[i][5]+1),float(current_car[i][6])+1][float(current_car[i][5]),float(current_car[i][6])]]
    xy_lst = [[float(current_car[i][5]),float(current_car[i][6])],[float(current_car[i][5])+2,float(current_car[i][6])+2]]
    measurements = np.asarray(xy_lst)
        
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
    # print(smoothed_state_means[0])
    # print(smoothed_state_means[1])
    # print()
    # plt.scatter(float(smoothed_state_means[0][0]),float(smoothed_state_means[0][2]),c='r')
    # plt.scatter(float(smoothed_state_means[1][0]),float(smoothed_state_means[1][2]),c='r')
    # plt.pause(1)
    
    xy_lst = []
# time.sleep(2)
# for i in range(len(smoothed_state_means)):
#     plt.scatter(float(smoothed_state_means[i][0]),float(smoothed_state_means[i][2]),c='r')
    # print(smoothed_state_means[i][0],smoothed_state_means[i][2])
    
print("Done time: ", time.time()- start)
# plt.figure(1)
# times = range(measurements.shape[0])
plt.show()