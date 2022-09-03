import numpy as np
import linfunc

quads = []
for down in (0,1):
    for right in (0,1):
        quads.append(np.load("./s"+str(30+2.5*down)+"e"+str(150+2.5*right)+"_dem_NumpyArray_Pickle", allow_pickle = True))
        

        
class grid:
    x_vals = [1.6,1.7,1.8,2.2,3.2,4.5,5.8,7.3,9.9,14.7,23.7]
    y_vals = [2,5,10,20,50,100,200,500,2000,10000,100000]
    
    def __init__(self, quads):
        grid = []
        for down in ((quads[0], quads[1]), (quads[2], quads[3])):
            for left, right in zip(down[0], down[1]):
                grid.append(list(left) + list(right))
        
        self.data = np.array(grid)
        
    def getpos(self, long, lat):
        if lat < 25 or lat >= 30 or long < 150 or long >= 155:
            print("WRONG")
            return 0
        return self.data[int(6000*((lat-25)/5))][int(6000*(long-150)/5)]
    
    def getfunc(self, long, lat):
        #assuming brisbane river is 4m above sea level
        difference = self.getpos(long, lat)-4
        return lambda x: 100000 if x + difference > 23.7 else 0 if x + difference < 1.6 else linfunc.linsample(grid.x_vals, grid.y_vals, [x + difference,x + difference,1])
        
    

    
dat = grid(quads)