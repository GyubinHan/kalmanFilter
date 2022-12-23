from random import uniform
from pyproj import CRS, Transformer
from shapely.geometry import Point, LineString
import matplotlib.pyplot as plt
import shapely.wkt
import numpy as np

import pandas as pd

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
import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient
import traceback
import pprint
import math
from matplotlib.animation import FuncAnimation
import os
from matplotlib.ticker import FuncFormatter
from pykalman import KalmanFilter as kf


# Start Point : Google headquarters:
google_lat = 37.422131
google_lon = -122.084801

# End Point : Apple headquarters
apple_lat = 37.33467267707233
apple_lon = -122.0089722675975

def reproject_point(lon, lat):
    in_crs = CRS.from_epsg(4326)
    out_crs = CRS.from_epsg(7131)
    proj = Transformer.from_crs(in_crs, out_crs, always_xy=True)
    x, y = proj.transform(lon, lat)
    # print(x,y)
    return x, y

def generate_random_points_on_line(number, line):
    points = []
    while len(points) < number:
        point = line.interpolate(uniform(0, line.length)).coords[0]
        points.append(point)
        
    return points    

start_point = Point(reproject_point(google_lon, google_lat))
end_point = Point(reproject_point(apple_lon, apple_lat))



straight_line = LineString([start_point, end_point]) 
# print(straight_line)
# print(generate_random_points_on_line(5, straight_line))


check_interpolation = LineString([(x1,y1),(x2,y2)]) # input value p1,p2
points = generate_random_points_on_line(100,check_interpolation) # interpolation갯수 조정



# for i in range(len(points)):
    # plt.scatter(points[i][0],points[i][1],c='g')

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



######################### latest landShifter  #########################

def laneShifter(x_lst,y_lst,theta,totalLaneNo,laneNumber, laneWidth):
    new_x_lst = []
    new_y_lst = []
    
    for i in range(0, len(x_lst)):
        new_x = x_lst[i] - np.sin(theta) * ((totalLaneNo * laneWidth / 2) - ((totalLaneNo-laneNumber) * laneWidth))
        #new_x2 = x_lst[i+1] - np.sin(theta) * (totalLaneNo * laneWidth / 2 - ((laneNumber - 1) * laneWidth))
        
        new_x_lst.append(new_x)
        #new_x_lst.append(new_x2)
        new_y = y_lst[i] + np.cos(theta) * ((totalLaneNo * laneWidth / 2) - ((totalLaneNo-laneNumber) * laneWidth))
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
                
        id_lst = [] 
        coord_lst = []
        theta = []
        
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

                ######## plot traffic information 
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
                            plt.plot(new_x,new_y,color='black')
                        elif j == totalLaneNo:
                            new_x,new_y = laneShifter(x_new_lst,y_new_lst,theta,totalLaneNo,j,laneWidth)
                            plt.plot(new_x,new_y, c='r')
                        else:
                            new_x,new_y = laneShifter(x_new_lst,y_new_lst,theta,totalLaneNo,j,laneWidth)
                            plt.plot(new_x,new_y,c='black')
                          

                            
        os.chdir("/Users/e8l-20210032/Downloads/addXY_new3/")
        os.getcwd()
        
        path = "Vehicle_Info__VISSIM_Time_"
        file_format = ".csv"
        csv_lst = []
        for i in range(900,1201):
            s = path+str(i)+file_format
            csv_lst.append(s)
        
        current_car = []  
        for c in csv_lst:
            f = open(c, 'r', encoding='utf-8' )     
            rdr = csv.reader(f)
            for line in rdr:
                #print(type(line[0])) # str
                # if line[0] == '1903':
                if line[0] == '1374': ######### 문제 해결 필요################
                    current_car.append(line)
                    
            f.close()
            
        temp = 900
        for i in range(len(current_car)):
            plt.scatter(float(current_car[i][5]),float(current_car[i][6]),c='b')
            plt.annotate(text=str(temp),xy=(float(current_car[i][5]),float(current_car[i][6])))
            temp += 1
  
        print(type(float(current_car[0][1])))
                    
        my_lst = []
        for i in range(len(current_car)-1):
            # plt.scatter(float(current_car[i][5]),float(current_car[i][6]),c = 'r')
            #my_lst.append((float(current_car[i][5]),float(current_car[i][6])))
            
            check_interpolation = LineString([(current_car[i][5],current_car[i][6]),(current_car[i+1][5],current_car[i+1][6])]) # input value p1,p2
            points = generate_random_points_on_line(10,check_interpolation) # interpolation갯수 조정

            
            
        # print(my_lst)  
        measurements = np.asarray(my_lst)




            
        initial_state_mean = [measurements[0, 0],
                            0,
                            measurements[0, 1],
                            0]

        transition_matrix = [[1, 1, 0, 0],
                            [0, 1, 0, 0],
                            [0, 0, 1, 1],
                            [0, 0, 0, 1]]

        observation_matrix = [[1, 0, 0, 0],
                            [0, 0, 1, 0]]

        kf1 = kf(transition_matrices = transition_matrix,
                        observation_matrices = observation_matrix,
                        initial_state_mean = initial_state_mean)

        # kf1 = kf(transition_matrices = [[1, 1], [0, 1]], observation_matrices = [[0.1, 0.5], [-0.3, 0.0]])

        kf1 = kf1.em(measurements, n_iter=5)
        (smoothed_state_means, smoothed_state_covariances) = kf1.smooth(measurements)

        # plt.figure(1)
        times = range(measurements.shape[0])

        # print(smoothed_state_means[5][0],smoothed_state_means[5][1])
        # plt.scatter(smoothed_state_means[5][0],smoothed_state_means[5][2],c = 'skyblue')
        

        ####################################### 2022-11-11까지 일했고 다음주에 해야함
        for i in range(len(measurements)):
            # plt.scatter(measurements[i][0],measurements[i][1],c='r')
            plt.scatter(smoothed_state_means[i][0].item(),smoothed_state_means[i][2].item(),c='skyblue')
            print(smoothed_state_means[i][0].item(),smoothed_state_means[i][2].item())
            print(float(current_car[i][5]),float(current_car[i][6]))
                    
                    


            
            #plt.pause(0.01)
        plt.show()
            

        
    except Exception as e:
        print(traceback.format_exc())
    finally:
        client.close()
        print('MongoDB Closed.')
 
if __name__ == "__main__":
    main()
