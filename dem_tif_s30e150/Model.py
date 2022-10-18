import numpy as np
import os
from matplotlib import pyplot as plt
import math

class grid:
    x_vals = [1.6,1.7,1.8,2.2,3.2,4.5,5.8,7.3,9.9,14.7,23.7]
    y_vals = [2,5,10,20,50,100,200,500,2000,10000,100000]

    river_pos = ((27.44469,153.10307),
                 (27.44266,153.05770),
                 (27.47443,153.04205),
                 (27.48435,152.99736),
                 (27.51269,153.00010),
                 (27.52624,152.97075),
                 (27.52705,152.93932),
                 (27.53831,152.92628))

    def __init__(self):
        grid = []
        quads = get_quads()
        for down in ((quads[0], quads[2]), (quads[1], quads[3])):
            for left, right in zip(down[0], down[1]):
                grid.append(list(left) + list(right))

        self.data = np.array(grid)

    def getpos(self, long, lat):
        """
        This function is used to get the altatude of a point.
        """

        lat *= -1

        if lat < 25 or lat >= 30 or long < 150 or long >= 155:
            print("WRONG")
            return 0
        point = self.data[int(6000*((lat-25)/5))][int(6000*(long-150)/5)]
        if point > 100:
            point /= 100
        return point

    def check_in_bounds(self, long, lat):
        """
        This function is used to determine if a point is close enough to the river for the model to work
        """

        lat *= -1

        dists = []

        for x in grid.river_pos:
            dist = math.sqrt((lat-x[0])**2 + (long-x[1])**2)
            # print(dist)
            if dist <= 0.03:
                dists.append(dist)
        if len(dists) == 0:
            return 2
        return min(dists)

    def getfunc(self, long, lat):
        """
        This function is used to get the flood rust function given a point
        """

        dist = self.check_in_bounds(long, lat)
        if dist == 2:
            return lambda x: 100000
        
        dist_diff = 20+40*((math.exp(250*(dist-0.028)))/(1+math.exp(250*(dist-0.028)))-0.5)

        #assuming brisbane river is 4m above sea level
        difference = self.getpos(long, lat)-4 + dist_diff
        return lambda x: 100000 if x + difference > 23.7 else 0 if x + difference < 1.6 else linsample(grid.x_vals, grid.y_vals, [x + difference,x + difference,1])[0]

def get_quads():
    quads = []
    cwd = os.getcwd()
    picklePathPrefix = ""

    if "/" in cwd:
        # Unix
        parent = cwd.split("/")[-1]
    else:
        # Windows
        parent = cwd.split("\\")[-1]

    if parent == "dem_tif_s30e150":
        picklePathPrefix = "./"
    elif parent == "FloodVisualisation" or parent == "uwsgi":
        picklePathPrefix = "./dem_tif_s30e150/"

    for down in (0,1):
        for right in (0,1):
            quads.append(np.load(picklePathPrefix + "s"+str(30+2.5*down)+"e"+str(150+2.5*right)+"_dem_NumpyArray_Pickle", allow_pickle = True))

    return quads

def line(point1, point2, x_val):
    if point1[0] == point2[0]:
        point1 = (point1[0] + 0.000001, point1[1])
    return (point1[1]-point2[1])/(point1[0]-point2[0])*x_val+(point1[1]-(point1[1]-point2[1])/(point1[0]-point2[0])*point1[0])

def linsample(x_vals, y_vals, arange):
    """
    linsample creates a linear segment model with segments equal to the number of data points - 1
    it then samples this model in arange, and returns those values as a list.

    Input
    -----
    x_vals : list<float>
        the x values of the data points
    y_vals : list<float>
        the y values of the data points
    arange : list<float>
        the range of x values you wish to sample, formatted (x_min, x_max, x_step_count)

    Returns
    -------
    list<float>
        the y values that the model maps from the given arange.
    """

    x_vals.append(x_vals[len(x_vals)-1])
    y_vals.append(y_vals[len(y_vals)-1])

    head = 0
    stepsize = (arange[1]-arange[0])/arange[2]
    out = []

    for step in range(arange[2]):
        x_val = arange[0] + stepsize*step
        while x_vals[head+1] < x_val:
            head += 1
        out.append(line((x_vals[head],y_vals[head]), (x_vals[head+1], y_vals[head+1]), x_val))

    x_vals.pop()
    y_vals.pop()

    return out

def disp(modl):
    TL_BOUND = [-27.3773, 152.9029]
    BR_BOUND = [-27.5990, 153.2002]
    long_dist = BR_BOUND[0] - TL_BOUND[0]
    lat_dist = BR_BOUND[1] - TL_BOUND[1]
    
    ret = np.zeros([100,100])
    
    for long in range(100):
        for lat in range(100):
            pos = TL_BOUND[0] +long_dist*(long/100), TL_BOUND[1] +lat_dist*(lat/100)
            ret[long,lat] = modl.getfunc(pos[1],pos[0])(2)
    plt.imshow(ret)


if __name__ == "__main__":
    dat = grid()
    #disp(dat)
    print(dat.getfunc(153.0277, -27.4777)(2))

