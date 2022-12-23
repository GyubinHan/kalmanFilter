from ast import Try
import enum
from errno import ENETUNREACH
from hashlib import new
from itertools import groupby
# from dbm import _Database
import json
import csv
from tkinter import N
from typing import final
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient
import traceback
import pprint
import math
from matplotlib.animation import FuncAnimation
import os

laneNo = 1
laneWidth = 3
laneQty = 3
totalWidth = laneQty * laneWidth
distance = 3
dn = (laneNo-1) * laneWidth + laneWidth/2

host = '172.16.28.221'
port = 27017


def left_position(x,y,theta, laneQty, laneWidth):
            
    new_x = x - np.sin(theta) * laneQty * laneWidth / 2
    new_y = y + np.cos(theta) * laneQty * laneWidth / 2
    return new_x, new_y 

def getCarPosition(x,y,laneNumber,laneWidth, theta):
    dn = (laneNo - 1) * laneWidth + laneWidth/2
    carPosX = x + dn * np.sin(theta)
    carPosY = y - dn * np.sin(theta)
    return carPosX, carPosY
######################### old landShifter  #########################
# def laneShifter(x_lst,y_lst,theta,totalLaneNo,laneNumber, laneWidth):
#     new_x_lst = []
#     new_y_lst = []
    
#     for i in range(0, len(x_lst)-1):
#         new_x = x_lst[i] - np.sin(theta) * (totalLaneNo * laneWidth / 2 - ((laneNumber - 1) * laneWidth))
#         #new_x2 = x_lst[i+1] - np.sin(theta) * (totalLaneNo * laneWidth / 2 - ((laneNumber - 1) * laneWidth))
        
#         new_x_lst.append(new_x)
#         #new_x_lst.append(new_x2)
#         new_y = y_lst[i] + np.cos(theta) * (totalLaneNo * laneWidth / 2 - ((laneNumber - 1) * laneWidth))
#         #new_y2 = y_lst[i+1] + np.cos(theta) * (totalLaneNo * laneWidth / 2 - ((laneNumber - 1) * laneWidth))
#         new_y_lst.append(new_y)
#         #new_y_lst.append(new_y2)
        
#     return new_x_lst, new_y_lst


######################### latest landShifter  #########################
def left_position(x,y,totalLaneNo,laneWidth,theta):
    #dn = (laneNo-1) * laneWidth + laneWidth/2
    new_x = x - np.sin(theta) * totalLaneNo * laneWidth
    new_y = y + np.cos(theta) * totalLaneNo * laneWidth
    return new_x, new_y

def laneShifter(x_lst,y_lst,theta,totalLaneNo,laneNumber, laneWidth):
    new_x_lst = []
    new_y_lst = []
    
    for i in range(0, len(x_lst)):
        new_x = x_lst[i] - np.sin(theta) * (totalLaneNo * laneWidth / 2 - ((laneNumber - 1) * laneWidth ))
        #new_x2 = x_lst[i+1] - np.sin(theta) * (totalLaneNo * laneWidth / 2 - ((laneNumber - 1) * laneWidth))
        
        new_x_lst.append(new_x)
        #new_x_lst.append(new_x2)
        new_y = y_lst[i] + np.cos(theta) * (totalLaneNo * laneWidth / 2 - ((laneNumber - 1) * laneWidth))
        #new_y2 = y_lst[i+1] + np.cos(theta) * (totalLaneNo * laneWidth / 2 - ((laneNumber - 1) * laneWidth))
        new_y_lst.append(new_y)
        #new_y_lst.append(new_y2)
        
    return new_x_lst, new_y_lst

def CurrentlaneShifter(x_lst,y_lst,theta,totalLaneNo,laneNumber, laneWidth,id_lst):
    new_x_lst = []
    new_y_lst = []
    car_position = []
    
    for i in range(0, len(x_lst)):
        new_x = x_lst[i] - np.sin(theta) * (totalLaneNo * laneWidth / 2 - ((laneNumber - 1) * laneWidth + laneWidth/2 ))
        #new_x2 = x_lst[i+1] - np.sin(theta) * (totalLaneNo * laneWidth / 2 - ((laneNumber - 1) * laneWidth))
        #new_x_lst.append(new_x)
        #new_x_lst.append(new_x2)
        car_position.append(new_x)
        new_y = y_lst[i] + np.cos(theta) * (totalLaneNo * laneWidth / 2 - ((laneNumber - 1) * laneWidth + laneWidth/2))
        #new_y2 = y_lst[i+1] + np.cos(theta) * (totalLaneNo * laneWidth / 2 - ((laneNumber - 1) * laneWidth))
        #new_y_lst.append(new_y)
        #new_y_lst.append(new_y2)
        car_position.append(new_y)
       
        
        
        
    return car_position


def main():
    try:
        client = MongoClient(
            host=host,
            port=port,
            # replica=replica set
            username='ndxpro',
            password='ndxpro123!',
            authSource='ndxpro'

        )
        
        # client = MongoClient('mongodb://ndxpro:ndxpro123!@172.16.28.221:27017/')
        db = client['ndxpro'] ## db name
        collection = db['entities']
        # print(collection)
        print('MongoDB Connected.')

        id_lst = [] 
        coord_lst = []
        final_lst = []
        totalLaneN_lst = []
        laneWidth_lst = []
        
        ax = plt.axes()
        ax.set_facecolor("grey")

        temp = 0 
        for data in collection.find():
            jtop = json.dumps(data)
            json_object = json.loads(jtop)
            
            
            j_coord = json_object['attribute']['https://uri-etsi-org/ngsi-ld/location']['value']['coordinates']
            id_lst.append(int(json_object["_id"]["_id"].replace("urn:ngsi-ld:Link:Link","")))
            coord_lst.append(j_coord)
            #theta_lst.append(json_object['attribute']['https://smartdatamodels-org/dataModel-Transportation/angle']['value'])
            laneWidth = json_object['attribute']['https://smartdatamodels-org/dataModel-Transportation/carriagewayWidth']['value']
            totalLaneNo = int(json_object['attribute']["https://smartdatamodels-org/dataModel-Transportation/totalLaneNumber"]['value'])
            
            totalLaneN_lst.append(int(json_object['attribute']["https://smartdatamodels-org/dataModel-Transportation/totalLaneNumber"]['value']))
            laneWidth_lst.append(json_object['attribute']['https://smartdatamodels-org/dataModel-Transportation/carriagewayWidth']['value'])
            
            
            
            
            ########## 팀장님 코드 ######################################################################
            # x_lst = []
            y_lst = []
            car_position = []
            test_position = []
            test_position.append(int(json_object["_id"]["_id"].replace("urn:ngsi-ld:Link:Link","")))
            test_position.append(int(json_object['attribute']["https://smartdatamodels-org/dataModel-Transportation/totalLaneNumber"]['value']))
            
            #test_position.append(json_object['attribute']['https://uri-etsi-org/ngsi-ld/location']['value']['coordinates'])
            
        
        lanePosition = []
        for i in range(len(id_lst)):
            for j in range(0,len(coord_lst[i])-1):
                rad = np.arctan2(coord_lst[i][j+1][1]-coord_lst[i][j][1],coord_lst[i][j+1][2]-coord_lst[i][j][2])
                print(rad)
            ################ plot final

                # for i in range(0, len(x_lst)-1):
                #     x_new_lst = []
                #     y_new_lst = []
                #     theta = np.arctan2(y_lst[i+1]-y_lst[i],x_lst[i+1]-x_lst[i])
                #     x_new_lst.append(x_lst[i])
                #     #x_new_lst.append(x_lst[i+1])
                                     
                #     y_new_lst.append(y_lst[i])
                #     #y_new_lst.append(y_lst[i+1])

                    
        # for i in range(len(id_lst)):
        #     print(id_lst[i])     
                    
                    
                    
        
        
        ####### final list
        for i in range(len(id_lst)):
            for j in range(len(coord_lst[i])):
                final_lst.append([id_lst[i],coord_lst[i][j][0],coord_lst[i][j][1],totalLaneN_lst[i],laneWidth_lst[i]]) # id, x, y, Total lane, lane width
            

        
        ######## read csv
        os.getcwd()
        os.chdir("/Users/e8l-20210032/Downloads/Info_Example/01.Vehicle_Info/")
        os.getcwd()
        
        path = "Vehicle_Info__VISSIM_Time_"
        file_format = ".csv"
        csv_lst = []
        for i in range(900,1201):
            s = path+str(i)+file_format
            csv_lst.append(s)
        
        
        
        # ########## read csv by line
        current_car = []  
        for c in csv_lst:
            f = open(c, 'r', encoding='utf-8' )     
            rdr = csv.reader(f)
            for line in rdr:
                #print(type(line[0])) # str
                
                if line[0] == '1374':
                    current_car.append(line)
            f.close()
        print(current_car)

        #theta = np.arctan2(v_num_lst[1][2]-v_num_lst[0][2],v_num_lst[1][1]-v_num_lst[0][1])
        
        
        ######## 특정 번호 읽기
        # v_num_lst = []
        # for i in range(len(final_lst)):
        #     if final_lst[i][0] == 102:
        #          v_num_lst.append(final_lst[i])
        
        
        
        ####################### 내일 할 일 애니메이션 수식 적용
        # v_x_lst = []
        # v_y_lst = []
        # for i in range(len(v_num_lst)):
        #     theta = np.arctan2(v_num_lst[i+1][2]-v_num_lst[i][2],v_num_lst[i+1][1]-v_num_lst[i][1])
        #     x,y = left_position(v_num_lst[i][1],v_num_lst[i][2],v_num_lst[i][3],v_num_lst[i][4],theta)
        #     v_x_lst.append(x)
        #     v_y_lst.append(y)
            
            
        # for i in range(len(v_x_lst)):
        #     car_x, car_y = getCarPosition(x,y,current_car[2],v_num_lst[i][4],theta)
        #     plt.scatter(car_x,car_y,c='purple')
        #     ######## animation part 
            # x = []
            # y = []
            # line, = plt.plot([],[],'bo')
            
            # def update(frame):
            #     x.append(frame)
            #     y.append(np.sin(frame))
            #     line.set_data(x, y)
            #     return line,


            # ani = FuncAnimation(plt, update, frames=np.linspace(0, 2*np.pi, 128))
           
                    
                    
        # plt.show()
        
        
        
    except Exception as e:
        print(traceback.format_exc())
    finally:
        client.close()
        print('MongoDB Closed.')
 
if __name__ == "__main__":
    main()

