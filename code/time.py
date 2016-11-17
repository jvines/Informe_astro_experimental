import glob

import matplotlib.cm as cm
import matplotlib.pyplot as plt
import scipy as sp
from astropy.io import fits

from obtain_time import obtain_time
from aperture_error import ap_phot, centroid
from zscale import zscale

paths1 = glob.glob("../data/dat.0*.fits")
paths1.sort()
paths1 = paths1[22::]
paths2 = glob.glob("../data/dat.[1-9]??.fits")
paths2.sort()
paths3 = glob.glob("../data/dat.1???.fits")
paths3.sort()
paths = paths1 + paths2 + paths3
fluxes = sp.zeros(len(paths))
ref_fluxes = sp.zeros_like(fluxes)
flux_final = sp.zeros_like(fluxes)
error = sp.zeros_like(fluxes)

time = obtain_time(paths)

x1 = 453  # 232; 411
y1 = 1564  # 671; 1838
SR1 = 45  # 30

x2 = 311
y2 = 1451
SR2 = 20

ap = 7
sky1 = 20
sky2 = 30

apr = 5.8
sky1r = 10
sky2r = 25

i = 0

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
    flx, err1 = ap_phot(stamp, cy, cx, ap, sky1, sky2)
    flxref, err2 = ap_phot(ref, cry, crx, apr, sky1r, sky2r)
    fluxes[i] = flx
    ref_fluxes[i] = flxref
    error[i] = err1
    i += 1

flux_final = fluxes / ref_fluxes

plt.clf()
plt.plot(time, fluxes, '.')
plt.errorbar(time, fluxes, yerr=error, fmt=None)
plt.xlabel('Tiempo [$s$]')
plt.ylabel('Cuentas [$e^2/ADU$]')
plt.title('Flujo de Wasp5 en el tiempo')
plt.savefig("flujo.pdf")
plt.show()
