import pandas as pd
import numpy as np
from scipy.spatial import ConvexHull
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt
from scipy import interpolate
import shapely
from pathlib import Path

num_tracks = 150
num_centerline_coords = 150

#All units in meters unless otherwise specified
track_max_size = 100 #This refers to the maximum side length of a square bounding the track area. E.g. 10 for a circular track of radius 5
track_min_size = 20

max_points=25 #Max number of points to spawn for the concave hull. Higher values leads to basically square tracks, small are more varied.
min_points=8 #Minimum number of points of the above

max_width=30
min_width=20

script_dir = Path(__file__).resolve().parent
output_dir_tr = script_dir / "tracks"
output_dir_cl = script_dir / "centerlines"

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


    #THIS SECTION ACTIVATES OBSTACLES BUT I DON'T KNOW HOW TO ENSURE THEY DON'T BLOCK THE WHOLE TRACK
    #obstacledata_array=np.random.rand((num_points*2), 2)
    
    #obstacledata_array[:, 0] = obstacledata_array[:, 0]*(np.random.randint(maxrandvalue_track)+addfactor_size)
    #obstacledata_array[:, 1] = obstacledata_array[:, 1]*(np.random.randint(maxrandvalue_track)+addfactor_size)
    

    hull = shapely.MultiPoint(trackdata_array)
    hull = shapely.concave_hull(hull, ratio=0.7, allow_holes=False)
    track_points = shapely.get_coordinates(hull).tolist()
    track_points = np.array(track_points)

    distances = np.sqrt(np.sum(np.diff(track_points, axis=0)**2, axis=1))
    t = np.insert(np.cumsum(distances), 0, 0)

    spline = make_interp_spline(t, track_points, bc_type="periodic") 

    t_smooth = np.linspace(0, t[-1], 550)
    smooth_points = spline(t_smooth)

    track_vectors = zip(smooth_points[:, 0], smooth_points[:, 1])
    df_trackvectors = pd.DataFrame(track_vectors)

    tck,u = interpolate.splprep(df_trackvectors.transpose(), s=0)
    unew = np.arange(0, 1.01, 0.01)
    out = interpolate.splev(unew, tck)

    maxrandvalue_width, addfactor_width = calculate_max(max_width, min_width)

    track_width = np.random.randint(maxrandvalue_width)
    width = (track_width+addfactor_width)

    #ALSO WITH THE OBSTACLE BIT
    #plt.scatter(obstacledata_array[:, 0], obstacledata_array[:, 1], color='black', marker='s', s=0.5, zorder=3)
    plt.xlim=track_max_size+max_width
    plt.ylim=track_max_size+max_width
    plt.plot(out[0], out[1], color='black', lw=width, clip_on=False)
    plt.plot(out[0], out[1], color='white', lw=(width-2),clip_on=False)
    plt.axis('equal')
    plt.axis('off')

    fig = plt.gcf() 
    ax = plt.gca()
    line = ax.get_lines()[-1]

    lw_points = line.get_linewidth()
    lw_pixels = lw_points * (fig.dpi/72)

    inv_transform = ax.transData.inverted()
    origin_m = inv_transform.transform((0, 0))
    offset_m = inv_transform.transform((lw_pixels, 0))

    total_width_m = offset_m[0] - origin_m[0]
    center_to_edge_m = total_width_m / 2.0

    #print(f"Total width: {total_width_m} m")
    #print(f"Centerline dist: {center_to_edge_m} m")

    smooth_points = np.insert(smooth_points, smooth_points.shape[1], center_to_edge_m, axis=1)
    smooth_points = np.insert(smooth_points, smooth_points.shape[1], center_to_edge_m, axis=1)
    print(type(smooth_points))
    print(smooth_points)

    header_str = "x_m\ty_m\tw_tr_right_m\tw_tr_left_m"

    plt.savefig(output_dir_tr / f"track_{i}.png")
    plt.close()
    

    np.savetxt(output_dir_cl / f"centerline_{i}.tsv", smooth_points, delimiter="\t", header=header_str)
    print(f"saved track #{i}")

    




    




