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

def laneShifter(x_lst,y_lst,theta,totalLaneNo,laneNumber, laneWidth):
    new_x_lst = []
    new_y_lst = []
    
    for i in range(0, len(x_lst)):
        new_x = x_lst[i] - np.sin(theta) * (totalLaneNo * laneWidth / 2 - ((laneNumber - 1) * laneWidth))
        #new_x2 = x_lst[i+1] - np.sin(theta) * (totalLaneNo * laneWidth / 2 - ((laneNumber - 1) * laneWidth))
        
        new_x_lst.append(new_x)
        #new_x_lst.append(new_x2)
        new_y = y_lst[i] + np.cos(theta) * (totalLaneNo * laneWidth / 2 - ((laneNumber - 1) * laneWidth))
        #new_y2 = y_lst[i+1] + np.cos(theta) * (totalLaneNo * laneWidth / 2 - ((laneNumber - 1) * laneWidth))
        new_y_lst.append(new_y)
        #new_y_lst.append(new_y2)
        
    return new_x_lst, new_y_lst


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
        
        temp = 0
        lenP = 0 
        id_lst = [] 
        coord_lst = []
        final_lst = []
        tuple_lst = []
        theta = []
        
        temp = 0
        
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
        
            
            
            
        
            x_lst = []
            y_lst = []
       
        
            
            ########## 팀장님 코드 ######################################################################
            for key,value in enumerate(json_object['attribute']['https://uri-etsi-org/ngsi-ld/location']['value']['coordinates']):
                
                
                #new_x,new_y = left_position(float(value[0]),float(value[1]),theta,totalLaneNo,laneWidth)
                
                x_lst.append(float(value[0]))
                y_lst.append(float(value[1]))
                #plt.plot(x_lst,y_lst,color='orange')
            ################ plot final
                
                
                #tuple_lst.append((float(value[0]),float(value[1])))
                #plt.plot(tuple_lst[key][0],tuple_lst[key][1],'red')
                #plt.plot(x_lst,y_lst,c='red')
                #print(len(x_lst))
                for i in range(0, len(x_lst)-1):
                    x_new_lst = []
                    y_new_lst = []
                    theta = np.arctan2(y_lst[i+1]-y_lst[i],x_lst[i+1]-x_lst[i])
                    x_new_lst.append(x_lst[i])
                    x_new_lst.append(x_lst[i+1])
                                     
                    y_new_lst.append(y_lst[i])
                    y_new_lst.append(y_lst[i+1])

                    
                    for j in range(0,totalLaneNo+1):
                        if j == 0:
                            new_x,new_y = laneShifter(x_new_lst,y_new_lst,theta,totalLaneNo,j,laneWidth)
                            #print(new_x,new_y,theta,totalLaneNo,j,laneWidth)
                            plt.plot(new_x,new_y,color='y')
                        else:
                            new_x,new_y = laneShifter(x_new_lst,y_new_lst,theta,totalLaneNo,j,laneWidth)
                            #print(new_x,new_y,theta,totalLaneNo,j,laneWidth)
                            
                            plt.plot(new_x,new_y,c='white')
                    
                    
                # for j in range(1,totalLaneNo+1):
                #     xaa,yaa = laneShifter(new_x,new_y,theta, totalLaneNo,j, laneWidth)
                #     print(xaa,yaa,theta,totalLaneNo,j, laneWidth)
                #     plt.plot(xaa,yaa,c='black')
                ############################################################################
                
                # for j in range(0,1):
                #     xaa,yaa = laneShifter(new_x,new_y,theta[i],totalLaneNo,j, laneWidth)
                #     print(xaa,yaa,theta[i],totalLaneNo,j, laneWidth)
                #     plt.plot(xaa,yaa)
        
            
            
    
            
                
            ######## animation part 
            # x = []
            # y = []
            # line, = plt.plot([],[],'bo')
            
            # def update(frame):
            #     x.append(frame)
            #     y.append(np.sin(frame))
            #     line.set_data(x, y)
            #     return line,


            # ani = FuncAnimation(plt, update, frames=np.linspace(0, 2*np.pi, 128))
            
                    
                    
        plt.show()
        
        
        
    except Exception as e:
        print(traceback.format_exc())
    finally:
        client.close()
        print('MongoDB Closed.')
 
if __name__ == "__main__":
    main()

