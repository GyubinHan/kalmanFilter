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

######################### old landShifter  #########################
def laneShifter_old(x_lst,y_lst,theta,totalLaneNo,laneNumber, laneWidth):
    new_x_lst = []
    new_y_lst = []
    
    for i in range(0, len(x_lst)-1):
        new_x = x_lst[i] - np.sin(theta) * (totalLaneNo * laneWidth / 2 - ((laneNumber - 1) * laneWidth))
        #new_x2 = x_lst[i+1] - np.sin(theta) * (totalLaneNo * laneWidth / 2 - ((laneNumber - 1) * laneWidth))
        
        new_x_lst.append(new_x)
        #new_x_lst.append(new_x2)
        new_y = y_lst[i] + np.cos(theta) * (totalLaneNo * laneWidth / 2 - ((laneNumber - 1) * laneWidth))
        #new_y2 = y_lst[i+1] + np.cos(theta) * (totalLaneNo * laneWidth / 2 - ((laneNumber - 1) * laneWidth))
        new_y_lst.append(new_y)
        #new_y_lst.append(new_y2)
        
    return new_x_lst, new_y_lst


######################### latest landShifter  #########################

def laneShifter(x_lst,y_lst,theta,totalLaneNo,laneNumber, laneWidth):
    new_x_lst = []
    new_y_lst = []
    
    for i in range(0, len(x_lst)):
        new_x = x_lst[i] - np.sin(theta) * ((totalLaneNo * laneWidth / 2) - ((laneNumber - 1) * laneWidth))
        #new_x2 = x_lst[i+1] - np.sin(theta) * (totalLaneNo * laneWidth / 2 - ((laneNumber - 1) * laneWidth))
        
        new_x_lst.append(new_x)
        #new_x_lst.append(new_x2)
        new_y = y_lst[i] + np.cos(theta) * ((totalLaneNo * laneWidth / 2) - ((laneNumber - 1) * laneWidth))
        #new_y2 = y_lst[i+1] + np.cos(theta) * (totalLaneNo * laneWidth / 2 - ((laneNumber - 1) * laneWidth))
        new_y_lst.append(new_y)
        #new_y_lst.append(new_y2)
        
    return new_x_lst, new_y_lst



def left_position(x,y,theta, laneQty, laneWidth):
            
        new_x = x - np.sin(theta) * laneQty * laneWidth / 2
        new_y = y + np.cos(theta) * laneQty * laneWidth / 2
        return new_x, new_y 




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

                    for j in range(1,totalLaneNo+1):
                        
                        ############# lane shifting new version
                        # if j == 0:
                        #     new_x,new_y = laneShifter(x_new_lst,y_new_lst,theta,totalLaneNo,j,laneWidth)
                        #     ax.plot(new_x,new_y,color='y')
                        # else:
                        #     new_x,new_y = laneShifter(x_new_lst,y_new_lst,theta,totalLaneNo,j,laneWidth)
                        #     ax.plot(new_x,new_y,c='black')
                        #     for j in range(0,totalLaneNo+1):
                        
                        ############# lane shifting old version
                        if j == 1:
                            new_x,new_y = laneShifter(x_new_lst,y_new_lst,theta,totalLaneNo,j,laneWidth)
                            ax.plot(new_x,new_y,color='y')
                        else:
                            new_x,new_y = laneShifter(x_new_lst,y_new_lst,theta,totalLaneNo,j,laneWidth)
                            ax.plot(new_x,new_y,c='black')                          
                            
                            
        os.getcwd()
        os.chdir("/Users/e8l-20210032/Downloads/addXY_new/")
        os.getcwd()
        
        path = "Vehicle_Info__VISSIM_Time_"
        file_format = ".csv"
        csv_lst = []
        for i in range(900,1201):
            s = path+str(i)+file_format
            csv_lst.append(s)
        
        
        
        
        
        ###################### read csv by line (working version)  ######################
        current_car = []  

        temp = 0
        for c in csv_lst:
            # f = open(c, 'r', encoding='utf-8' )     
            rdr = pd.read_csv(c,names=["CarNo","LinkNo","CurrentLane","Lane","Distance(M)","X-Coordinate","Y-Coordinate"])
            current_car.append(rdr)
            for i in range(len(current_car)):
                df = pd.DataFrame(current_car[i])
                ax.scatter(x = df['X-Coordinate'],y = df['Y-Coordinate'], c = df['CarNo'])
                # ax.pause(0.01)
                
                
        
        plt.show()
        ######################################################################################


        # for c in csv_lst:
        #     f = open(c, 'r', encoding='utf-8' )     
        #     rdr = csv.reader(f)
        #     for line in rdr:
        #         #print(type(line[0])) # str
        #         if line[0] == '1053':
        #             #current_car.append(line+c.replace("Vehicle_Info__VISSIM_Time_","").replace(".csv",""))
        #             current_car.append(1)
        #             #plt.scatter(float(line[5]),float(line[6]),c = 'r')
        #             #plt.annotate(line[0],float(line[5]),float(line[6]))
        
        #     # f.close()
        
        # # plt.show()
        
        # carNo = []
        # texts = []
        # for i in range(len(current_car)):
        #     # plt.scatter(float(current_car[i][5]),float(current_car[i][6]))
        #     #carNo.append(current_car[i][0])
        #     texts = current_car[i][7]
        #     # plt.text(float(current_car[i][5]),float(current_car[i][6]),texts, c = 'black')
            # plt.annotate(txt, current_car[i][5],current_car[i][6])
        
            
        # plt.scatter(float(current_car[i][5]),float(current_car[i][6]))
        #     plt.annotate(txt, current_car[i][5],current_car[i][6])
            
        # plt.show()
          
          
          
        #################### testing tag in scatter plot

        # for c in csv_lst:
        # # f = open(c, 'r', encoding='utf-8' )     
        # # rdr = csv.reader(f)
        #     rdr = pd.read_csv(c,names=["CarNo","LinkNo","CurrentLane","Lane","Distance(M)","X-Coordinate","Y-Coordinate"])
        #     for line in rdr:
        #         #rdr["csvNo"] = csv_lst.replace("Vehicle_Info__VISSIM_Time_","").replace(".csv","")
        #         current_car.append(rdr)
     
        # # print(current_car)
        
        
        # for i in range(len(current_car)):
        #     plt.scatter(float(current_car[i][5]),float(current_car[i][6],),c = current_car[i][0])
        # plt.show()
        

    
        # # ############################### Final plotting animation
        # # # fig = ax.figure(figsize=(7,5))

        # # animation = FuncAnimation(fig,animation_func, interval=10,repeat=False)
        # # plt.get_current_fig_manager().full_screen_toggle()
        # # plt.show()
        
        
        # for i in range(len(current_car)):
        #     x_lst.append(current_car[i][5])
        #     y_lst.append(current_car[i][6])
        #     #animation_lst.append(current_car[i][5])
        #     #animation_lst.append(current_car[i][6])
        #     ax.scatter(x_lst[i],y_lst[i],c='b')
        #     ax.pause(1.5)
        # plt.show()
                    

        
    except Exception as e:
        print(traceback.format_exc())
    finally:
        client.close()
        print('MongoDB Closed.')
 
if __name__ == "__main__":
    main()
