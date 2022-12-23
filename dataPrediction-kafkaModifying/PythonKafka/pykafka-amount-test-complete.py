from kafka import KafkaProducer
from json import dumps
import time
from kafka import KafkaConsumer
import msgpack

producer = KafkaProducer(acks=0, compression_type='gzip', bootstrap_servers=['172.16.28.220:19092'],
                         value_serializer=lambda x: dumps(x).encode('utf-8'))

start = time.time()

# for i in range(1000):
#     data = {'name': 'Hello' + str(i+100)}
#     producer.send('amount-test3', value= data)
#     producer.flush() 



from kafka import KafkaConsumer
from json import loads
from kafka.serializer import Deserializer

# topic, broker list
consumer = KafkaConsumer('amount-test3',
    bootstrap_servers=['172.16.28.220:19092'],
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='amount-group2',
#  value_deserializer=lambda x: loads(x.decode('utf-8')),
    value_deserializer = msgpack.unpackb,
    consumer_timeout_ms=1000
)

# consumer list를 가져온다
print('[begin] get consumer list')
temp = 0
while True:
    for message in consumer:
        print("Topic: %s, Partition: %d, Offset: %d, Key: %s, Value: %s" % (
            message.topic, message.partition, message.offset, message.key, message.value
        ))
        
print('[end] get consumer list')