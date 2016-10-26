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
ref_fluxes = sp.zeros_like(fluxes)

x1 = 453  # 232; 411
y1 = 1564  # 671; 1838
SR1 = 45  # 30

x2 = 311
y2 = 1451
SR2 = 25 / 2.
i = 0

ap = 7
sky1 = 20
sky2 = 30

apr = 6
sky1r = 15
sky2r = 20

bias = fits.getdata("../master/master_bias.fits", 1)
flats = fits.getdata("../master/master_flats.fits", 1)

for p in paths:
    sci = fits.getdata(p, 1)
    print(p)
    final = sp.divide(sci - bias, flats)
    stamp = final[y1 - SR1:y1 + SR1, x1 - SR1:x1 + SR1]
    ref = final[y2 - SR2:y2 + SR2, x2 - SR2:x2 + SR2]
    cx, cy = centroid(stamp)
    crx, cry = centroid(ref)
    flx = ap_phot(stamp, cy, cx, ap, sky1, sky2)
    flxref = ap_phot(ref, cry, crx, apr, sky1r, sky2r)
    fluxes[i] = flx
    ref_fluxes[i] = flxref
    i += 1

final_flux = sp.divide(fluxes, ref_fluxes)
plt.clf()
plt.plot(range(len(paths)), final_flux, '.')
plt.savefig("flujo.pdf")
plt.show()
