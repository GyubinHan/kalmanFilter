
from kafka import KafkaProducer
from json import dumps
import time
import json
from kafka import KafkaProducer
from kafka import KafkaConsumer
from json import loads
import datetime

producer = KafkaProducer(acks=0,
                         compression_type = 'gzip',
                         bootstrap_servers=['172.16.28.217:9092'],
                         value_serializer= lambda x: dumps(x).encode('utf-8'))


start = time.time()
for i in range(10):
    data = {'name': 'Hello' + str(i+120)}
    producer.send('kafka.group.test02', value= data)
    producer.flush() 


print("Producing time", (time.time()-start)) # 걸리는 시간
print("Producing Done")




################### kafka consumer #######################
from json import loads
# import datetime
# consumer = KafkaConsumer("kafka.group.test02",
#                          bootstrap_servers = ['172.16.28.217:9092'],
#                          auto_offset_reset='earliest',
#                          group_id = 'connectiong-test-group',
#                          value_deserializer = lambda x: loads(x.decode('utf-8')),
#                          consumer_timeout_ms=1000)
#                         #  enable_auto_commit=True,


consumer = KafkaConsumer("kafka.group.test02", group_id ='connectiong-test-group',bootstrap_servers=['172.16.28.217:9092'],auto_offset_reset='earliest',
                         value_deserializer = lambda x: loads(x.decode('utf-8')), enable_auto_commit=True,consumer_timeout_ms=1000,key_deserializer = lambda x: 
                         )

start = time.time()
print("Start : ",start)

# while True:
for message in consumer:
    topic = message.topic
    partition = message.partition
    offset = message.offset
    value = message.value
    timestamp = message.timestamp
    datetimeobj = datetime.datetime.fromtimestamp(timestamp/10000)
    # print(message.value)
    print("Topic:{}, partition:{}, offset:{}, value:{}, datetimeobj:{}".format(topic,partition,offset,value,timestamp,datetimeobj))
    


print("Elapsed time = ", (time.time()- start))

