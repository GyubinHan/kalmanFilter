from kafka import KafkaConsumer
import time
from kafka import KafkaProducer
import json
from json import dumps
from json import load

consumer = KafkaConsumer("dataModelPython",group_id="dataModel_test_group",bootstrap_servers=['172.16.28.217:9092'],consumer_timeout_ms=1000, 
                         value_deserializer= json.load)

start = time.time()
for message in consumer:
    print(message.value)
print("End consuming")
time.sleep(1)

producer = KafkaProducer(acks=0,
                         bootstrap_servers=["172.16.28.217:9092"],
                         compression_type='gzip',
                         value_serializer= lambda x: dumps(x).encode('utf-8'))

for i in range(3):
    data = {'name {}'.format(str(i)): 'Hello' + str(i)}
    producer.send("dataModelPython",data)
    producer.flush()

print("End :",time.time()-start)



for new_message in consumer:
    print(message.value)