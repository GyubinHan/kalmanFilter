import numpy as np
import pandas as pd
from pykalman import KalmanFilter as kf
import os
import csv
import matplotlib.pyplot as plt


# current_measurement = np.array([[np.float32(3.0)],[np.float32(4.0)]])

# def update(mean1, var1, mean2, var2):
#     new_mean = (var2 * mean1 + var1 * mean2) / (var1 + var2)
#     new_var = 1/ (1 / var1 + 1 / var2)
#     return [new_mean, new_var]


# def predict(mean1,var1,mean2,var2):
#     new_mean = mean1 + mean2
#     new_var = var1 + var2
#     return [new_mean,new_var]


# measurement = [5.,6.,7.,8.,9.,10.]
# motion = [1., 1., 2., 1., 1.]
# measurement_sig = 4.
# motion_sig = 2.
# mu = 0.
# sig = 10000.


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
    
# print(my_lst)  
measurements = np.asarray(my_lst)

# for i in measurements:
#     print(i)




    
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

# kf1 = kf(transition_matrices = [[1, 1], [0, 1]], observation_matrices = [[0.1, 0.5], [-0.3, 0.0]])

kf1 = kf1.em(measurements, n_iter=5)
(smoothed_state_means, smoothed_state_covariances) = kf1.smooth(measurements)

plt.figure(1)
times = range(measurements.shape[0])


for i in range(9):
    print(float(current_car[i][5]),float(current_car[i][6]),smoothed_state_means[i][0],smoothed_state_means[i][2])

# for i in range(len(current_car)):
    # plt.scatter(float(current_car[i][5]),float(current_car[i][6]),c='orange')

# plt.plot(times, measurements[:, 0], 'bo',
#          times, measurements[:, 1], 'ro',
#          times, smoothed_state_means[:, 0], 'b--',
#          times, smoothed_state_means[:, 2], 'r--',)
# plt.show()


# for i in range(len(measurements)):
#     # plt.scatter(measurements[i][0],measurements[i][1],c='r')
#     # plt.scatter(smoothed_state_means[i][0],smoothed_state_means[i][1],c='b')
#     print(type(smoothed_state_means[i][0].item()))
# plt.show()
