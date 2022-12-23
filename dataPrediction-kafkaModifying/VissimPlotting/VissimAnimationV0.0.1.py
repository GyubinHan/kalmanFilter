from ast import Try
import enum
from errno import ENETUNREACH
from hashlib import new
from itertools import groupby
# from dbm import _Database
import json
import csv
from optparse import Option
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
from matplotlib.ticker import FuncFormatter


laneNo = 1
laneWidth = 3
laneQty = 3
totalWidth = laneQty * laneWidth
distance = 3
dn = (laneNo-1) * laneWidth + laneWidth/2

host = '172.16.28.221'
port = 27017
fig, ax = plt.subplots()
#ax2 = plt.subplot(212,sharex=ax)
ax = plt.axes()
ax.set_facecolor("grey")



def left_position(x,y,theta, laneQty, laneWidth):
            
            new_x = x - np.sin(theta) * laneQty * laneWidth / 2
            new_y = y + np.cos(theta) * laneQty * laneWidth / 2
            return new_x, new_y 

def scientific(x, pos):
    # x:  tick value - ie. what you currently see in yticks
    # pos: a position - ie. the index of the tick (from 0 to 9 in this example)
    return '%.2E' % x



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
                
                x_lst.append(float(value[0]))
                y_lst.append(float(value[1]))
            ################ plot final
                
                
                #plt.plot(x_lst,y_lst,c='red')
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
                            #print(new_x,new_y)
                            #print(new_x,new_y,theta,totalLaneNo,j,laneWidth)
                            ax.plot(new_x,new_y,color='y')
                            ax.ticklabel_format(axis='x',useOffset=False, style='plain')
                            #ax.ticklabel_format(axis='y',useOffset=False, style='plain')
                            #plt.show()
                            
                            #plt.axis('auto')
                            #ax.set_xlim(-5748200,-5746880)
                            #ax.set_ylim(-968400,-967000)
                            #plt.show()
                            #plt.axis(-5700000)
                            #plt.relim()
                            #ax.autoscale_view()

                        else:
                            new_x,new_y = laneShifter(x_new_lst,y_new_lst,theta,totalLaneNo,j,laneWidth)
                            #print(new_x,new_y)
                            #print(new_x,new_y,theta,totalLaneNo,j,laneWidth)
                            ax.plot(new_x,new_y,c='black')
                            ax.ticklabel_format(axis='x',useOffset=False, style='plain')
                            
                            #plt.xlim(-5748200,-5746880)
                            #plt.ylim(-968400,-967000)
                            #plt.axis('auto')
                            #plt.axis([-57482000,-57468800,-968400,-967000])
                            #ax.relim()
                            #ax.autoscale_view()
                            
                            
        os.getcwd()
        os.chdir("/Users/e8l-20210032/Downloads/addXY_new3/")
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
        x_lst = []
        y_lst = []
        
        
        plt.pause(10)
        
        #################################### animation result
        for i in range(len(current_car)):
            
            x_lst.append(float(current_car[i][5]))
            y_lst.append(float(current_car[i][6]))
            
            #ax.scatter(float(current_car[i][5]),float(current_car[i][6]),c='blue',marker='o')
            #plt.pause(1)
        # def animation_func(i):
        #     # interpolation = x_lst*(1-i) + x_lst*i    
        #     # #for i in range(len(x_lst)):
        #     ax.scatter(x_lst[i],y_lst[i],c='r',alpha= 0.5)

    
        # ############################### Final plotting animation
        # # fig = ax.figure(figsize=(7,5))

        # animation = FuncAnimation(fig,animation_func, interval=1,repeat=False)
        # plt.get_current_fig_manager().full_screen_toggle()
        
        
        
        for i in range(len(current_car)):
            x_lst.append(current_car[i][5])
            y_lst.append(current_car[i][6])
            #animation_lst.append(current_car[i][5])
            #animation_lst.append(current_car[i][6])
            plt.scatter(x_lst[i],y_lst[i],c='b')
            plt.pause(1)
        mng = plt.get_current_fig_manager()
        mng.full_screen_toggle()
        plt.show()
        
         # def animation_func(i):
        # #     # interpolation = x_lst*(1-i) + x_lst*i    
        # #     # #for i in range(len(x_lst)):
        # #     ax.scatter(x_lst[i],y_lst[i],c='r',alpha= 0.5)

            
       
           
        
        
    except Exception as e:
        print(traceback.format_exc())
    finally:
        client.close()
        print('MongoDB Closed.')
 
if __name__ == "__main__":
    main()

