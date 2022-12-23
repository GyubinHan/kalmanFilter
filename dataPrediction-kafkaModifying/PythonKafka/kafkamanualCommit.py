import json
from json import dumps
from kafka import KafkaProducer
from kafka import KafkaConsumer, TopicPartition
import time
import datetime
import os 
from json import loads



producer = KafkaProducer(acks=1,
                         compression_type='gzip',
                         bootstrap_servers=["172.16.28.220:39092","172.16.28.220:19092","172.16.28.220:29092","172.16.28.220:49092","172.16.28.220:59092"],
                         value_serializer= lambda x: dumps(x).encode('utf-8'))

# for i in range(3):
#     data = {"connect check": str(i+1000)}
#     check = producer.send("pykafka-test-topic2",data).get()
#     print(check)
#     producer.flush()
    
print("Producer data send completed")


def forgiving_json_deserializer(v):
    if v is None:
        try:
            return json.loads(v.decode('utf-8'))
        except json.decoder.JSONDecodeError:
            log.exception('Unable to decode: %s', v)
            return None

consumer = KafkaConsumer("pykafka-test-topic2",
                        bootstrap_servers=["172.16.28.220:39092","172.16.28.220:19092","172.16.28.220:29092","172.16.28.220:49092","172.16.28.220:59092"],
                        group_id="None",
                        value_deserializer = lambda x : forgiving_json_deserializer(x),
                        auto_offset_reset ="earliest",
                        enable_auto_commit= False)
consumer.subscribe(['pykafka-test-topic2'])

from kafka import TopicPartition , OffsetAndMetadata


import json


consumer = KafkaConsumer ('hello_world1',bootstrap_servers = ['localhost:9092'],
value_deserializer=lambda m: json.loads(m.decode('utf-8')),group_id='connection-test-group',auto_offset_reset='latest',
                          enable_auto_commit =False)

while True:
    for message in consumer:
        print(message)
        print("The value is : {}".format(message.value))
        print("The key is : {}".format(message.key))
        print("The topic is : {}".format(message.topic))
        print("The partition is : {}".format(message.partition))
        print("The offset is : {}".format(message.offset))
        print("The timestamp is : {}".format(message.timestamp))
        tp=TopicPartition(message.topic,message.partition)
        om = OffsetAndMetadata(message.offset+1, message.timestamp)
        consumer.commit({tp:om})
        print('*' * 100)
