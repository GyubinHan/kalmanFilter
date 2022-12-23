
import threading
import queue
from queue import PriorityQueue
import numpy as np
from kafka import KafkaProducer,KafkaConsumer
from json import dumps, loads


def producer():

    consumer = KafkaConsumer("threading-v1",
                         bootstrap_servers=['172.16.28.220:19092'],
                         group_id = 'threading-group',
                         auto_offset_reset='earliest',
                         enable_auto_commit = True,
                         value_deserializer = lambda x: loads(x.decode('utf-8')),
                         consumer_timeout_ms = 600)
    count = 0 
    while True:

        lock.acquire() # 전역 변수 접근을 금지합니다.

        for message in consumer:    
            if not q.full(): # 큐가 꽉차지 않았다면

                q.put_nowait((message.value['time'],message.value['vehicles'])) # 큐에 데이터를 넣습니다.
                print(f'push item {count}')
                count += 1
            

            lock.release() # 이제 전역 변수 접근을 할 수 있습니다.

        if count == 10: break

    print('thread 1 exit')


def consumer():
    count = 0 
    while True:
        lock.acquire()  # 전역 변수 접근을 금지합니다.

        if not q.empty(): # 큐가 비어있지 않다면
            item = q.get_nowait() # 큐에서 데이터를 꺼냅니다.
            print(f'get item {item}')

        lock.release()  # 이제 전역 변수 접근을 할 수 있습니다.
        count += 1
        if count == 3: break

    print('thread 2 exit')




# producer = KafkaProducer(acks=0,
#                          bootstrap_servers=['172.16.28.220:19092'],
#                          compression_type='gzip',
#                          value_serializer= lambda x: dumps(x).encode('utf-8'))


# for i in range(6):
#     data = {
#         "time": i,
#         "vehicles": [
#         {
#             "id": 991,
#             "linkId": 90,
#             "lane": 1,
#             "location": 11.484880201098946,
#             "speed": 41.113604245609324,
#             "position": [
#                 -5747062.111932379,
#                 -967533.2282339633
#             ]
#         },
#         {
#             "id": 1032,
#             "linkId": 102,
#             "lane": 4,
#             "location": 118.61874747898035,
#             "speed": 42.51976193580154,
#             "position": [
#                 -5747565.153118768,
#                 -967207.7858925589
#             ]
#         }]
#         }
#     producer.send("threading-v1",data)
    
# print("Producing done")



# 큐의 최대 크기는 3입니다.
q = PriorityQueue(5)

lock = threading.Lock()  # 뮤텍스 객체를 전역으로 선언하여 스레드간에 공유하도록 합니다.


t1 = threading.Thread(target=producer) # 큐에 데이터를 넣는 스레드입니다.
t1.start()
t2 = threading.Thread(target=consumer) # 큐에서 데이터를 꺼내는 스레드입니다.
t2.start()

t1.join()
t2.join()

print('main exit')