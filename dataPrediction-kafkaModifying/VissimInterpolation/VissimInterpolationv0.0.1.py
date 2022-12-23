from random import uniform
from pyproj import CRS, Transformer
from shapely.geometry import Point, LineString
import matplotlib.pyplot as plt
import shapely.wkt
import numpy as np
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


x1 = -5747872.696975
x2 = -5747817.747455
y1 = -967926.685685
y2 = -967895.899235

check_interpolation = LineString([(x1,y1),(x2,y2)]) # input value p1,p2
points = generate_random_points_on_line(100,check_interpolation) # interpolation갯수 조정
plt.scatter(x1,y1,c='r')
plt.scatter(x2,y2,c='r')



for i in range(len(points)):
    plt.scatter(points[i][0],points[i][1],c='g')
plt.show()