import numpy as np
import os
import csv
import pandas as pd
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation
import plotly.express as px
import sys
from matplotlib.animation import PillowWriter
from easing import easing

#from pyproj import CRS, transformerfrp
#from shapely.geometry import Point, LineString


os.getcwd()
os.chdir("/Users/e8l-20210032/Downloads/addXY/")
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
        
        if line[0] == '651':
            current_car.append(line)
    f.close()
    
            
x_lst = []
y_lst = []
#line = plt.scatter([],[],color = 'skyblue',marker='o')

# def update(frames):    
#     for i in range(len(current_car)):
#         x_lst.append(x_lst[i])
#         y_lst.append(y_lst[i])
#     line.set_data(x_lst,y_lst)
# graphanimation = FuncAnimation(fig=plt, func=update, frames=x_lst,)

animation_lst = [] 
for i in range(len(current_car)):
    x_lst.append(current_car[i][5])
    y_lst.append(current_car[i][6])
    animation_lst.append(current_car[i][5])
    animation_lst.append(current_car[i][6])
    #plt.scatter(current_car[i][5],current_car[i][6],c='b')
    #plt.pause(0.01)
    
# print(animation_lst)
# for i in range(len(animation_lst)):
#     plt.scatter(animation_lst[i][0],animation_lst[i][1])


# fig = plt.gcf()

# scat, = plt.scatter([],[],c='green')
# def update_plot(t):

#     interpolation = animation_lst[t]*(1-t) + animation_lst[t+1]
#     scat.set_offsets(interpolation.T)
    
#     return scat,

# FuncAnimation(plt,update_plot,frames=10,interval=50)
# # plt.show()





# line, = plt.scatter([],[],'ro')

# metadata = dict(title='Movie',artist='codinglikemad')
# writer = PillowWriter(fps=150, metadata=metadata)

# line, = plt.scatter([],[],'r0')
# with writer.saving(plt, "plottingAnimation.gif",len(x_lst)):
#     for i in range(len(x_lst)):
#         line.set_data(x_lst[i],y_lst[i])
        
#         writer.grab_frames()

############################### working plotting animation
fig = plt.figure(figsize=(7,5))
line, = plt.plot([],[],c='green')
list_x = []
list_y = []
def animation_func(i):
    list_x.append(x_lst[i])
    list_y.append(y_lst[i])
    line.set_data(list_x, list_y)
    
animation = FuncAnimation(fig,animation_func, frames = 3)
# fig.tight_layout()
plt.show()
###############################

################################## test 3  ##################################
# originalpoint = np.asarray([[x_lst[0]],[y_lst[0]]])
# newPoints = np.asarray([[x_lst[1]],[y_lst[1]]])

# OriginP = [[x_lst[0]],[y_lst[0]]]
# NewP = [[x_lst[1]],[y_lst[1]]]


# def update_plot(t):
#     interpolation = originalpoint*(1-t) + newPoints*t
#     scat.set_offsets(interpolation.T)
#     return scat,


# #plt.scatter(originalpoint[0,:],originalpoint[1,:], color='red')
# #plt.scatter(newPoints[0,:],newPoints[1,:], color='blue')
# scat = plt.scatter([],[],color = 'green')

# FuncAnimation(fig,update_plot2,frames=np.arange(0,1,0.01))

# df = pd.DataFrame(animation_lst)
# df2 = pd.DataFrame(x_lst,y_lst,index=['x'])

# print(df2)
# easing.Eased(df2).scatter_animation2d(n=3,speed=0.5,destination='testing.gif')


################################## test 5  ##################################
# origin = np.array([x_lst[0],y_lst[0]])
# new = np.array([x_lst[1],y_lst[1]])
# print(origin)
# print(type(new[0]))

# def animation_func(i):
#         # interpolation = x_lst*(1-i) + x_lst*i    
#         # #for i in range(len(x_lst)):
#         origin_p = np.array([x_lst[i],y_lst[i]],dtype=float)
#         new_P = np.array([x_lst[i+1],y_lst[i]],dtype=float)
#         interpolation = origin_p*(1-i) + new_P* i
#         scat.set_offsets(interpolation.T)
#         return scat

    
#         ############################### Final plotting animation
#         # fig = ax.figure(figsize=(7,5))
# plt.scatter(x_lst[0],y_lst[0],c='r',alpha= 0.5)
# plt.scatter(x_lst[1],y_lst[1],c='r')
# scat = plt.scatter([],[],c='green')
# animation = FuncAnimation(fig,animation_func, frames=4,interval=1,repeat=False)
# # plt.get_current_fig_manager().full_screen_toggle()
# plt.show()



################################## test 6 ##################################
# originalPoints = np.asarray([[1,2,3,4,5,6],[2,4,6,8,10,12]])
# newPoints = np.asarray([[1,2,3,4,5,6],[2,4,6,8,10,12]]) + 20
# plt.scatter(originalPoints[0,:],originalPoints[1,:], color='red');
# plt.scatter(newPoints[0,:],newPoints[1,:], color='blue');

# import matplotlib.animation as animation

# def update_plot(t):
#     interpolation = originalPoints*(1-t) + newPoints*t
#     scat.set_offsets(interpolation.T)
#     return scat,

# fig = plt.gcf()
# plt.scatter(originalPoints[0,:],originalPoints[1,:], color='red')
# plt.scatter(newPoints[0,:],newPoints[1,:], color='blue')
# scat = plt.scatter([], [], color='green')
# animation.FuncAnimation(fig, update_plot, frames=np.arange(0, 1, 0.01))
# plt.show()

################################## test 5  ##################################
