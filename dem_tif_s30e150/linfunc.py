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