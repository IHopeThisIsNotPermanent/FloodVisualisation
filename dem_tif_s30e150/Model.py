import numpy as np
import linfunc
from matplotlib import pyplot as plt
import math

quads = []
for down in (0,1):
    for right in (0,1):
        quads.append(np.load("./s"+str(30+2.5*down)+"e"+str(150+2.5*right)+"_dem_NumpyArray_Pickle", allow_pickle = True))

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

    def __init__(self, quads):
        grid = []
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

        for x in grid.river_pos:
            dist = math.sqrt((lat-x[0])**2 + (long-x[1])**2)
            # print(dist)
            if dist <= 0.03:
                return True
        return False

    def getfunc(self, long, lat):
        """
        This function is used to get the flood rust function given a point
        """

        if not self.check_in_bounds(long, lat):
            return lambda x: 100000

        #assuming brisbane river is 4m above sea level
        difference = self.getpos(long, lat)-4
        return lambda x: 100000 if x + difference > 23.7 else 0 if x + difference < 1.6 else linfunc.linsample(grid.x_vals, grid.y_vals, [x + difference,x + difference,1])[0]



if __name__ == "__main__":
    dat = grid(quads)
    print(dat.getfunc(153.0277, -27.4777)(2))
