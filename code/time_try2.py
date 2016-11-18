import glob

import matplotlib.cm as cm
import matplotlib.pyplot as plt
import scipy as sp
from astropy.io import fits

from obtain_time import obtain_time
from aperture_error_try2 import ap_phot, centroid
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
error1 = sp.zeros_like(fluxes)
error2 = sp.zeros_like(fluxes)

time = obtain_time(paths)

##### TARGET
x1 = 411  # 232; 411
y1 = 1838  # 671; 1838
SR1 = 30  # 30

ap = 9
sky1 = 20
sky2 = 25

##### REF

x2 = 340
y2 = 543
SR2 = 45

apr = 8
sky1r = 25
sky2r = 30

i = 0

bias1 = fits.getdata("../master/master_bias.fits", 1)
flats1 = fits.getdata("../master/master_flats.fits", 1)

bias2 = fits.getdata("../master/master_bias.fits", 4)
flats2 = fits.getdata("../master/master_flats.fits", 4)

for p in paths:
    sci1 = fits.getdata(p, 1)
    sci2 = fits.getdata(p, 4)
    print(p)

    final1 = sp.divide(sci1 - bias1, flats1)
    final2 = sp.divide(sci2 - bias2, flats2)

    stamp = final1[y1 - SR1:y1 + SR1, x1 - SR1:x1 + SR1]
    ref = final2[y2 - SR2:y2 + SR2, x2 - SR2:x2 + SR2]

    cx, cy = centroid(stamp)
    crx, cry = centroid(ref)

    flx, err1 = ap_phot(stamp, cy, cx, ap, sky1, sky2)
    flxref, err2 = ap_phot(ref, cry, crx, apr, sky1r, sky2r)

    fluxes[i] = flx
    ref_fluxes[i] = flxref
    error1[i] = err1
    error2[i] = err2
    i += 1

flux_final = fluxes / ref_fluxes

plt.clf()
plt.plot(time, ref_fluxes, '.')
# plt.errorbar(time, fluxes, yerr=error1, fmt=None)
plt.xlabel('Tiempo [$s$]')
plt.ylabel('Cuentas [$ADU$]')
plt.title('Cuociente entre el flujo de Wasp5 y una\nestrella\
 de referencia en el tiempo')
plt.savefig("flujo.pdf")
plt.show()
