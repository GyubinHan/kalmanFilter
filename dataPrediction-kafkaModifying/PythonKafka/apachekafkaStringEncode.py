from kafka import KafkaProducer
from kafka import KafkaConsumer
import json
from json import loads,dumps
import datetime
import time
import numpy as np


producer = KafkaProducer(acks=0,
                         bootstrap_servers="172.16.28.220:19092",
                         value_serializer= lambda x: str(x).encode("utf-8"),
                         compression_type='gzip')


# for i in range(10):
#     data = {"key {}".format(str(i)):"test {}".format(str(i))}
#     producer.send("string-test",data)
#     producer.flush()
    
    
# print("producing done")



consumer = KafkaConsumer("string-test", group_id ='string-group',bootstrap_servers=['172.16.28.220:19092'],auto_offset_reset='earliest',
                         value_deserializer = lambda x: str(x,'utf-8'), enable_auto_commit=True,consumer_timeout_ms=1000,
                         )


consumer.subscribe("string-test")
while True:
    for message in consumer:
        print("partitions is ",message.partition," value is ",message.value)
        # message_lst.append(message.value)
print("Consuming done")

# print(type(message_lst[0]))