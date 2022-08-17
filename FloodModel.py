import random, math


class FloodModel:
    def __init__(self):
        pass
    
    def sample(self, coord):
        growth_coefficent = random.choice(range(1,10))
        elevation_coefficent = random.choice((1,1,2,3,10))
        return lambda x : math.e**(x/growth_coefficent)+math.e**elevation_coefficent