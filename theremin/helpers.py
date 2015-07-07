################################################################################
# Multithreaded Blinking Theremin - helper.py
#
# Created by VIPER Team 2015 CC
# Authors: L.F. Cerfeda, L. Cominelli
################################################################################

# Constrain a number to be within a range and maps it from one range to another.
# It is a merge of Constrain() and Map() Arduino functions

def map_range(x, in_min, in_max, out_min, out_max):
    if x < in_min:
        x = in_min    
    elif x > in_max: 
        x = in_max
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min