import numpy as np
from pykalman import KalmanFilter as kf
from queue import PriorityQueue
from kafka import KafkaConsumer,KafkaProducer 
from json import dumps, loads
import logging

que = PriorityQueue()
lst = [[0,0]]
lst.append([1,1])
lst.append([2,2])

# que.put(input[0])
# que.put(input[1])
# que.put(input[2])

# print(que.get())
# print(que.get())
# print(que.get())

logger = logging.getLogger("kalman")
logger.setLevel(logging.INFO)



sourceTopic = 'three-input-source'
bootstrap_servers = ['172.16.28.218:19092']

producer = KafkaProducer(acks=0,bootstrap_servers=bootstrap_servers,
                         compression_type='gzip',
                         value_serializer= lambda x: dumps(x).encode('utf-8'))


consumer = KafkaConsumer(sourceTopic,bootstrap_servers=bootstrap_servers,
                         enable_auto_commit=True,
                         auto_offset_reset='earliest',
                         value_deserializer= lambda x: loads(x.decode('utf-8')))



for i in range(len(lst)):
    data = {"i": f"{lst[i]}"}
    
    producer.send(sourceTopic, data)

print("producing done")


for message in consumer:
    new_message = message.value.copy()
    que.put(new_message,0)
    # new_message.clear()
    
    if que.__sizeof__ == 3:
        print(que.get())
        print(que.get())
        print(que.get())
    # print(new_message)        


measurements = np.asarray(input)
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

kf1 = kf1.em(measurements, n_iter=5)
(smoothed_state_means, smoothed_state_covariances) = kf1.smooth(measurements)
(filtered_state_means, filtered_state_covariances) = kf1.filter(measurements)

print(filtered_state_means)
# filtered_state_means = np.zeros((len(measurements), 4))
# filtered_state_covariances = np.zeros((len(measurements), 4, 4))

# for i in range(len(measurements)):
#     if i == 0:
#         filtered_state_means[i] = initial_state_mean
#         filtered_state_covariances[i] = initial_state_covariance
#         print(filtered_state_means)
        
#     else:
#         filtered_state_means[i], filtered_state_covariances[i] = (
#         kf1.filter_update(
#             filtered_state_means[i-1],
#             filtered_state_covariances[i-1],
#             observation = measurements_masked[i])
#         )
#         (smoothed_state_means, smoothed_state_covariances) = kf1.smooth(measurements)
#         (filtered_state_means, filtered_state_covariances) = kf1.filter(measurements)
        

#         print(filtered_state_means)



