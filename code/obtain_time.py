import numpy as np
from astropy.io import fits
import ast
import glob

paths1 = glob.glob("../data/dat.0*.fits")
paths1.sort()
paths1 = paths1[22::]
paths2 = glob.glob("../data/dat.[1-9]??.fits")
paths2.sort()
paths3 = glob.glob("../data/dat.1???.fits")
paths3.sort()
paths = paths1 + paths2 + paths3

def obtain_time(path):
    
    time = np.zeros(len(path))
    for i in range(len(time)):
        hdr = fits.getheader(path[i], 1)
        hr = hdr["TIME-OBS"]
        hour = 3600 * float(hr[0:2]) + 60 * float(hr[3:5]) + float(hr[6:])
        time[i] = hour
   
    time = time - time[0]

    return time
