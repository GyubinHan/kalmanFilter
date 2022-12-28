from pykalman.datasets import  load_robot
from pykalman import KalmanFilter as kf
from pykalman import UnscentedKalmanFilter 


data = load_robot()

# print(data.observations.shape[0])


import pykalman
import numpy as np

value = [[0,0],[1,1]]
measurements = np.asarray(value)
measurements_masked = np.ma.masked_invalid(measurements)

initial_state_mean = [measurements[0, 0],
                    0,
                    measurements[0, 1],
                    0]
initial_state_covariance = [[ 10, 0, 0, 0], 
                            [  0, 1, 0, 0],
                            [  0, 0, 1, 0],
                            [  0, 0, 0, 1]]

transition_matrix = [[1, 1, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, 1],
                    [0, 0, 0, 1]]

observation_matrix = [[1, 0, 0, 0],
                    [0, 0, 1, 0]]

kf1 = kf(transition_matrices = transition_matrix,
                observation_matrices = observation_matrix,
                initial_state_mean = initial_state_mean)

kf1 = kf1.em(measurements, n_iter=10)
kf1.observation_covariance = kf1.observation_covariance * 10
(smoothed_state_means, smoothed_state_covariances) = kf1.smooth(measurements)
(filtered_state_means, filtered_state_covariances) = kf1.filter(measurements)

# means, covariances = kf1.smooth(measurements)
# print(means)
# print(smoothed_state_means)
print(filtered_state_means)


filtered_state_means = np.zeros((len(measurements), 4))
filtered_state_covariances = np.zeros((len(measurements), 4, 4))

for i in range(len(measurements)):
    if i == 0:
        filtered_state_means[i] = initial_state_mean
        filtered_state_covariances[i] = initial_state_covariance
    else:
        filtered_state_means[i], filtered_state_covariances[i] = (
        kf1.filter_update(
            filtered_state_means[i-1],
            filtered_state_covariances[i-1],
            observation = measurements_masked[i])
        )
        print(filtered_state_means[i])
# (filtered_state_means, filtered_state_covariances) = kf.filter(measurements)
# (smoothed_state_means, smoothed_state_covariances) = kf.smooth(measurements)

# print(filtered_state_means)
# print(smoothed_state_means)



# ukf = UnscentedKalmanFilter(lambda x, w: x + np.sin(w), lambda x, v: x + v, observation_covariance=0.1)
# (filtered_state_means, filtered_state_covariances) = ukf.filter(measurements)
# (smoothed_state_means, smoothed_state_covariances) = ukf.smooth(measurements)

# print(filtered_state_means)
# print(smoothed_state_means)
