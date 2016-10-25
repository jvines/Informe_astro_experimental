from astropy.io import fits
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import scipy as sp
import glob
from zscale import zscale
from aperture import centroid, ap_phot

paths1 = glob.glob("../data/dat.0*.fits")
paths1.sort()
paths1 = paths1[22::]
paths2 = glob.glob("../data/dat.[1-9]??.fits")
paths2.sort()
paths3 = glob.glob("../data/dat.1???.fits")
paths3.sort()
paths = paths1 + paths2 + paths3
fluxes = sp.zeros_like(paths)

x = 411
y = 1838
SR = 48
i = 0
ap = 10
sky1 = 25
sky2 = 30

bias = fits.getdata("../master/master_bias.fits", 1)
flats = fits.getdata("../master/master_flats.fits", 1)

for p in paths:
    sci = fits.getdata(p, 1)
    print(p)
    final = sp.divide(sci - bias, flats)
    stamp = final[y -SR:y + SR, x - SR:x + SR]
    cx, cy = centroid(stamp)
    flx = ap_phot(stamp, cy, cx, ap, sky1, sky2)
    fluxes[i] = flx
    i += 1

plt.clf()
plt.plot(range(len(paths)), fluxes, '.')
plt.savefig("flujo.pdf")
plt.show()
