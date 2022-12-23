
import os

import yaml
# sourceTopic = os.environ['SOURCE_TOPIC']

# targetTopic = os.environ['TARGET_TOPIC']

# kafka_url = os.environ['KAFKA_URL'].split(',')

# consumer_group = os.environ['CONSUMER_GROUP']

# kalman_number = os.environ['KALMAN_NUMBER']

# kalman_log = os.environ['KALMAN_LOG']



with open('docker-compose.yml') as f:
    yml = yaml.load(f, Loader=yaml.FullLoader)
print(yml['services']['data-prediction0']['environment']['SOURCE_TOPIC'])
print(yml['services']['data-prediction0']['environment']['TARGET_TOPIC'])
print(yml['services']['data-prediction0']['environment']['KAFKA_URL'].split(','))

print(yml['services']['data-prediction0']['environment']['CONSUMER_GROUP'])
print(yml['services']['data-prediction0']['environment']['KALMAN_NUMBER'])
print(yml['services']['data-prediction0']['environment']['KALMAN_LOG'])

# ##testd
sourceTopic =  'kalman-10-source'
targetTopic =  'kalman-10-target'
kafka_url =  ['172.16.28.218:19092','172.16.28.218:29092','172.16.28.218:39092','172.16.28.218:49092','172.16.28.218:59092']
print(type(kafka_url))
url = '172.16.28.218:19092,172.16.28.218:29092,172.16.28.218:19092,172.16.28.218:19092,172.16.28.218:19092'
# print(url.split(','))
consumer_group =  'kafka-8'
kalman_number =  3
kalman_log = 'kalmanlog3.log'