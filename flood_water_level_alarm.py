#input: river water level and given elevation
#output: a tuple, (a,b): a is the flood's severity,
# a has three value,1,2,3: minor, moderate and major
# b shows whether the current place is danger or not.
# 1 for danger, 0 for safe


minor=1
moderate=2
major=3

danger=1
safe=0

def flood_detector(river_level, input_elevation):
    
    if (river_level >= 1.7) and (river_level < 2.6) :
        
        if river_level > input_elevation:

            return (minor, danger)
        
        return (minor, safe)
    
    if (river_level >= 2.6) and (river_level < 3.5) :
        
        if river_level > input_elevation:
            
            return (moderate, danger)

        return (moderate, safe)
    
    if river_level >= 3.5:
        if river_level > input_elevation:
            return (major, danger)
        return (major, safe)
    
    return 0
