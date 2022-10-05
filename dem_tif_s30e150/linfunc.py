import numpy as np


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

class FailSegment:
    def __init__(self, start, end, value):
        """
        This class just represents 1D segments which have a value. it supports a couple of operations 
        between segments.
        
        Parameters
        ----------
        start : float
            the starting value, must be less than the end value
        end : float
            the end value.
        value : float
            the value of this segment
        
        """
        self.start = start
        self.end = end
        self.value = value
    
    def __le__(self, other):
        return self.start <= other.start
    
    def __lt__(self, other):
        return self.start < other.start
    
    def __str__(self):
        return "(" + str(self.start) + ", " + str(self.end) + ", " + str(self.value) + ")"
    
    def collide(self, other):
        """
        checks if two segments overlap.
        """
        return max(self.start, other.start) < min(self.end, other.end)
    
    def compose(self, other):
        """
        If segments were funcions, this is just adding together the functions.
        so like {f(x)=1, 0<x<2} + {f(x)=1, 1<x<3} = {f(x)=1, 0<x<1} + {f(x)=2, 1<x<2} + {f(x)=1, 2<x<3}
        Parameters
        ----------
        other : FailSegment
            The other fail segment you wish to compose this one with.
        Returns
        -------
        tuple<FailSegment>
            the failsegments in reverse order, after a compose
        """
        values = [0,self.value + other.value,0]
        
        if self.start < other.start:
            values[0] = self.value
        if self.start > other.start:
            values[0] = other.value
            
        if self.end < other.end:
            values[2] = other.value
        if self.end > other.end:
            values[2] = self.value
        
        return (FailSegment(min(self.end, other.end), max(self.end, other.end), values[2]),
                FailSegment(max(self.start, other.start), min(self.end, other.end), values[1]),
                FailSegment(min(self.start, other.start), max(self.start, other.start), values[0]))
                
    
    def merge(self, other):
        return FailSegment(min(self.start, other.start), max(self.end, other.end), self.value)
    
    
class SegmentGraph:
    def __init__(self):
        """
        This function just optimises composing lots of segments, assuming the value of each segment is 1.
        """
        self.vals = []
        self.buff = []
        self.integral = 0
        
    def buffer(self, values):
        self.buff += values
        
    def add(self, value):
        self.buff.append(value)
        
    def update(self):
        if len(self.buff) == 0:
            return
        self.vals = [0, ] * len(self.buff)*2
        firsts = list(np.sort([x.start for x in self.buff]))
        seconds = list(np.sort([x.end for x in self.buff]))
        vals_index = 0
        firsts_index = 0
        seconds_index = 0
        count = 0
        self.integral = 0
        start = firsts[0]
        """
        Basically how this algorithm works, is it keeps track of 2 lists, a list of the first x_position of the 
        segments, and the list of the second value of the second x_position of the segments.
        it the remembers what x value it is up to, and check to see if the next closest value is a first or a second
        if its a first, this means you increase the count, if its a second you decrease.
        
        """
        while firsts_index < len(firsts):
            
            if vals_index == len(self.vals):
                self.vals += [0,] * len(self.vals)
                
            if firsts[firsts_index] < seconds[seconds_index]: #If the first part of a segment comes first
                count += 1
                self.vals[vals_index] = (firsts[firsts_index], count)
                firsts_index += 1
                self.integral += (self.vals[vals_index][0]-start)*self.vals[vals_index][1] #This line starts summing the integral
                start = self.vals[vals_index][0]
                vals_index += 1
            elif firsts[firsts_index] > seconds[seconds_index]: #If the second part of a segment comes first
                count -= 1
                self.vals[vals_index] = (seconds[seconds_index], count)
                seconds_index += 1
                self.integral += (self.vals[vals_index][0]-start)*self.vals[vals_index][1]
                start = self.vals[vals_index][0]
                vals_index += 1
            elif firsts[firsts_index] == seconds[seconds_index]: #If they come at the same time.
                seconds_index += 1
                firsts_index += 1
            
        
        while seconds_index < len(seconds): # if we have ran out of firsts, there are only seconds left.
            
            if vals_index == len(self.vals):
                self.vals += [0,] * len(self.vals)
            
            count -= 1
            self.vals[vals_index] = (seconds[seconds_index], count)
            seconds_index += 1
            
            vals_index += 1
            
        if 0 in self.vals: #remove the zeros from the list
            self.vals = self.vals[:self.vals.index(0)]