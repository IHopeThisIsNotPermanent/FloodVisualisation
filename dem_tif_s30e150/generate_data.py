from Model import grid
from linfunc import linsample
import numpy as np
import json

LAT = [-27.3773, -27.5990]
LONG = [152.9029, 153.2002]

CONST = 1 / 1200

def years_to_weight(years):
    # 10, 20, 50, 100, 500
    # 1-0.8, 0.8-0.6, 0.6-0.4, 0.4-0.2, 0.2-0
    if years > 500:
        return 0
    return linsample([0,10,20,50,100,500],[1,0.8,0.6,0.4,0.2,0],[years, years, 1])[0]

if __name__ == "__main__":
    lat = LAT[0]
    long = LONG[0]

    quads = []
    for down in (0,1):
        for right in (0,1):
            quads.append(np.load("./s"+str(30+2.5*down)+"e"+str(150+2.5*right)+"_dem_NumpyArray_Pickle", allow_pickle = True))

    m = grid(quads)

    print("Time to die")

    a = []

    while lat > LAT[1]:
        while long < LONG[1]:
            a.append([lat, long, years_to_weight(m.getfunc(long, lat)(2))])
            long += CONST
        long = LONG[0]
        lat -= CONST

    print(len(a))

    with open("../data.txt", "w") as f:
        f.write(json.dumps(a))
