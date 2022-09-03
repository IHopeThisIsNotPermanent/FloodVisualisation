
from osgeo import gdal, ogr

import numpy as np

from matplotlib import pyplot as plt

import pickle as pkl

step1 = gdal.Open('s30e150_dem.tif', gdal.GA_ReadOnly)
GT_input = step1.GetGeoTransform()
step2 = step1.GetRasterBand(1)
img_as_array = step2.ReadAsArray()

height, width = img_as_array.shape


quads = []

for down in (0,1):
    for right in (0,1):
        temp = [[img_as_array[x][y] for y in range(int(down*height/2), int((down+1)*height/2))] for x in 
                                             range(int(right*width/2), int((right+1)*width/2))]
        fileObject = open("./s"+str(30+2.5*down)+"e"+str(150+2.5*right)+"_dem_NumpyArray_Pickle", 'wb')
        print(np.array(temp).shape)
        pkl.dump(np.array(temp), fileObject)


# 00 01 10 11
size1,size2=img_as_array.shape

