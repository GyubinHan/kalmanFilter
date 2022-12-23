from kafka import KafkaConsumer
from json import loads
from json import dumps
from kafka import KafkaProducer


def on_send_success(record_metadata):
    print("topic : {} , partition : {} , offset : {}".\
          format( record_metadata.topic , record_metadata.partition , record_metadata.offset))

class KafkaWrapper():
    def __init__(self,) :
        self.producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))
    
    
    def consume(self, topic , group):
        consumer = KafkaConsumer(bootstrap_servers=['172.16.28.220:19092','172.16.28.220:29092','172.16.28.220:39092','172.16.28.220:49092','172.16.28.220:59092'],
                                      group_id=group,
                                      value_deserializer=lambda x: loads(x.decode('utf-8')))
        consumer.subscribe(topic)
        for message in consumer:
            print ("topic=%s partition=%d offset=%d: key=%s value=%s" % (message.topic, message.partition,
                                          message.offset, message.key,
                                          message.value))
            data = {group : str(message.offset)}
            
            producer = KafkaProducer(bootstrap_servers=['172.16.28.220:19092','172.16.28.220:29092','172.16.28.220:39092','172.16.28.220:49092','172.16.28.220:59092'],
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))
            producer.send( "result", value = data ).add_callback(on_send_success)
            
class ServiceInterface():
    def __init__(self):
        self.kafka_wrapper = KafkaWrapper()

    def start(self, topic , group):
        self.kafka_wrapper.consume(topic , group)
class ServiceA(ServiceInterface):
    pass

class ServiceB(ServiceInterface):
    pass
    
from multiprocessing import Process
def main():
    serviceA = ServiceA()
    serviceB = ServiceB()

    jobs=[]
    # The code works fine if I used threading.Thread here instead of Process
    jobs.append(Process(target=serviceA.start, args=("my_topic","SR1",))) # my_topic
    jobs.append(Process(target=serviceB.start, args=("my-topic2","SR3",))) # my-topic

    for job in jobs:
        job.start()
        

    for job in jobs:
        job.join()
if __name__ == "__main__":
    main()