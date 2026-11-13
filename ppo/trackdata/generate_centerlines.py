import pandas as pd
import numpy as np
from scipy.spatial import ConvexHull
from scipy.interpolate import make_interp_spline

num_tracks = 1
num_centerline_coords = 150

#All units in meters unless otherwise specified
track_max_size = 100 #This refers to the maximum side length of a square bounding the track area. E.g. 10 for a circular track of radius 5
track_min_size = 20

max_points=15 #Max number of points to spawn for the convex hull. Higher values leads to basically square tracks, small are more varied.
min_points=7 #Minimum number of points of the above

max_width=10
min_width=5

def calculate_max(maximumvalue, minimumvalue):
    maxrandvalue=(maximumvalue-minimumvalue)
    addfactor=(minimumvalue)
    return(maxrandvalue,addfactor)

maxrandvalue_track, addfactor_track = calculate_max(max_points, min_points)
maxrandvalue_size, addfactor_size = calculate_max(track_max_size, track_min_size)

for i in range(0, num_tracks):
    
    #Defining the x/y coords and 
    num_points = np.random.randint(maxrandvalue_track)
    num_points = (num_points+addfactor_track)

    trackdata_array=np.random.rand(num_points, 2)



    trackdata_array[:, 0] = trackdata_array[:, 0]*(np.random.randint(maxrandvalue_track)+addfactor_size)
    trackdata_array[:, 1] = trackdata_array[:, 1]*(np.random.randint(maxrandvalue_track)+addfactor_size)
    #trackdata_array[:, 2]= (trackdata_array[:, 2])*(min_width)+(max_width-min_width)
    #trackdata_array[:, 2] = np.clip(trackdata_array[:, 2], min_width, max_width)
    

    hull = ConvexHull(trackdata_array)

    track_points = trackdata_array[hull.vertices]

    track_points = np.vstack([track_points, track_points[0]])

    distances = np.sqrt(np.sum(np.diff(track_points, axis=0)**2, axis=1))
    t = np.insert(np.cumsum(distances), 0, 0)

    spline = make_interp_spline(t, track_points, bc_type="periodic") 

    t_smooth = np.linspace(0, t[-1], 100)
    smooth_points = spline(t_smooth)



    




