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


lst = []
lst.append([1,2])
lst.append([3,4])

smoothed = kalmanfilter(lst)
print(smoothed)