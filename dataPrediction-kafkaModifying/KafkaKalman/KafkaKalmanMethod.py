import numpy as np
import pandas as pd
import json
import csv
import os
from kafka import KafkaProducer, KafkaConsumer
from kafka.admin import KafkaAdminClient,NewTopic
from json import dumps, loads




def file_reader(path,file_name,number,file_type):
    current_car = []
    os.chdir(path)
    c = file_name + str(number) + "."+ file_type
    
    f = open(c,"r",encoding='utf-8')
    rdr = csv.reader(f)
    
    
    for line in rdr:
        current_car.append(line)
    f.close()    
    return current_car


def kafka_topic_creator(topic,bootstrap_server,client):
    admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_server,
                                    client_id=client)
    topic_list = []
    topic_list.append(NewTopic(name="example_topic", num_partitions=3, replication_factor=3))
    admin_client.create_topics(topic_list,validate_only=False)

    

def kafka_producer(bootstrap_server,topic,data):
    producer = kafka_producer(acks=0,
                              bootstrap_servers=[bootstrap_server],
                              compression_type='gzip',
                              value_serializer = lambda x: dumps(x).encode('utf-8'))
    
    producer.send(topic, data)
    
def kafka_consumer(topic,bootstrap_server):
    consumer = KafkaConsumer(topic,bootstrap_servers=[bootstrap_server],
                             auto_offset_rest='earliest',
                             enable_auto_commit=True,
                             value_deserializer = lambda x: loads(x.decode('utf-8')))
    


path = "/Users/e8l-20210032/Downloads/addXY_new3/"
file_name = "Vehicle_Info__VISSIM_Time_"
number = 900
type = 'csv'

current_car = file_reader(path,file_name,number,type)

print(current_car)


for data in current_car:
    kafka_producer("172.16.28.220:19092","topic",data)
    
print("producing done")