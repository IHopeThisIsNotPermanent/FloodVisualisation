import math


def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

class SpatialRainfall:
    """
    Note: this model for the rainfall extrapolation does not take into 
    consideration any historical data, or research about the nature of 
    these sorts of models.
    Later iterations should do this.
    """
    def __init__(self, historical_data):
        self.historical_data = historical_data
        
    def predict(self, points, data):
        """
        
        Inputs
        ------
        points : list<2Dcoords>
            the list of points you wish to sample
        data : list<(2Dcoord, value)>
        """
        
        ret = []
        for point in points:
            min_dist = -1
            min_val = 0
            for measurement in data:
                distance = dist(measurement[0], point)
                if distance < min_dist or min_dist == -1:
                    min_dist = distance
                    min_val = measurement[1]
            ret.append(min_val)
        
        return ret
    
    