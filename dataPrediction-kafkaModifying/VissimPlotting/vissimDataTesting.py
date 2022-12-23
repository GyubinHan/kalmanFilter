import numpy as np

def left_position(x,y,totalLaneNo,laneWidth,theta):
    #dn = (laneNo-1) * laneWidth + laneWidth/2
    new_x = x - np.sin(theta) * totalLaneNo * laneWidth
    new_y = y + np.cos(theta) * totalLaneNo * laneWidth
    return new_x, new_y

def laneShifter(x_lst,y_lst,theta,totalLaneNo,laneNumber, laneWidth):
    new_x_lst = []
    new_y_lst = []
    
    # for i in range(0, len(x_lst)):
    new_x = x_lst - np.sin(theta) * (totalLaneNo * laneWidth / 2 - ((laneNumber - 1) * laneWidth )+ laneWidth/2)
    #new_x2 = x_lst[i+1] - np.sin(theta) * (totalLaneNo * laneWidth / 2 - ((laneNumber - 1) * laneWidth))
    
    new_x_lst.append(new_x)
    #new_x_lst.append(new_x2)
    new_y = y_lst + np.cos(theta) * (totalLaneNo * laneWidth / 2 - ((laneNumber - 1) * laneWidth) + laneWidth/2)
    #new_y2 = y_lst[i+1] + np.cos(theta) * (totalLaneNo * laneWidth / 2 - ((laneNumber - 1) * laneWidth))
    new_y_lst.append(new_y)
    #new_y_lst.append(new_y2)
        
    return new_x_lst, new_y_lst


x_lst = [-5747515.385446,-5747572.4095815131]
y_lst = [-967315.506949,-967182.79163300258]

theta = np.arctan2(y_lst[1]-y_lst[0],x_lst[1]-x_lst[0])
x,y = laneShifter(x_lst[0],y_lst[0],theta,5,3,3.2)
print(x,y) # [-5747518.325536605] [-967316.7702253885]

total_n = 5
lw = 3.2
ln = 3
theta = np.arctan2(y_lst[1]-y_lst[0],x_lst[1]-x_lst[0])



loriginx = x_lst[0] - (total_n*lw/2)*np.sin(theta)
loriginy = y_lst[0] + (total_n*lw/2)*np.cos(theta)


dx = loriginx + (lw*(ln-1)+lw/2)*np.sin(theta)
dy = loriginy - (lw*(ln-1)+lw/2)*np.cos(theta)

print(dx,dy) # -5747515.385446 -967315.506949




# new_x_lst = []
# new_y_lst = []

# for i in range(0,5):
#     new_x_lst.append(x - np.sin(theta) * (5 * 3.2 / 2 - ((i - 1) * 3.2 )))
#     new_y_lst.append(y + np.cos(theta) * (5 * 3.2 / 2 - ((i - 1) * 3.2 )))

# #print(new_x_lst,new_y_lst)
     


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# link no = 102
# ['651', '102', '3', '29.14036711183899', '44.60653965536181', '-5747526.8893015385', '-967288.7334116326']
# ['651', '102', '3', '41.52770798119429', '44.582314603996345', '-5747531.77950005', '-967277.3521914725']
# ['651', '102', '3', '53.89702510675352', '44.47676870003012', '-5747536.662583258', '-967265.9875311373']
# ['651', '102', '3', '66.22421015975588', '44.27896368158695', '-5747541.529033825', '-967254.6615808366']
# ['651', '102', '3', '78.4786499314482', '43.95300267459773', '-5747546.366766456', '-967243.402467323']
# ['651', '102', '3', '90.66166467988684', '43.76470351416044', '-5747551.176302353', '-967232.2089775718']
# ['651', '102', '3', '102.80718816115356', '43.683065550960016', '-5747555.9710376775', '-967221.0499339837']
# ['651', '102', '3', '114.93908359461098', '43.666581569933356', '-5747560.760393006', '-967209.9034115506']
# ['651', '102', '3', '127.1396397009656', '44.17742239581997', '-5747565.576853773', '-967198.69380518']
# ['651', '102', '3', '139.48209603673317', '44.688263221706585', '-5747570.449333043', '-967187.353823956']



# origin data
# d = 72.18483405230636
# distance test data to see the plot right
d = 29.14036711183899
# d = 
#d_lst = [29.14036711183899,41.52770798119429,53.89702510675352,66.22421015975588,78.4786499314482,90.66166467988684,102.80718816115356,114.93908359461098,127.1396397009656,139.48209603673317]

d_lst = [29.14036711183899,
41.52770798119429,
53.89702510675352,
66.22421015975588,
78.4786499314482,
90.66166467988684,
102.80718816115356,
114.93908359461098,
127.1396397009656,
139.48209603673317]

loriginx = x_lst[0] - (total_n*lw/2)*np.cos(theta)
loriginy = y_lst[0] + (total_n*lw/2)*np.sin(theta)


dx = loriginx + (lw*(ln-1)+lw/2)*np.cos(theta)
dy = loriginy - (lw*(ln-1)+lw/2)*np.sin(theta)


dxfinal = dx + d * np.cos(theta)
dyfinal = dy + d * np.sin(theta)


finalPointX = []
finalPointY = []

for i in range(len(d_lst)):
    finalPointX.append(dx + d_lst[i]* np.cos(theta))
    finalPointY.append(dy + d_lst[i]* np.sin(theta))
    
# for i in range(len(finalPointY)):
#     print(finalPointX[i],finalPointY[i])