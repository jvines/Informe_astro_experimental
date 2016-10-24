import scipy as sp
from astropy.io import fits
import matplotlib.pyplot as plt


def zscale(img,  trim = 0.05, contr=1, mask=None):
    """Returns lower and upper limits found by zscale algorithm for improved contrast in astronomical images.

:param mask: bool ndarray
    True are good pixels, pixels marked as False are ignored
:rtype: (min, max)
    Minimum and maximum values recommended by zscale
"""


    if not isinstance(img, sp.ndarray):
        img = sp.array(img)
    if mask is None:
        mask = (sp.isnan(img)==False)

    itrim = int(img.size*trim)
    x = sp.arange(mask.sum()-2*itrim)+itrim

    sy = sp.sort(img[mask].flatten())[itrim:img[mask].size-itrim]
    a,b = sp.polyfit(x, sy, 1)

    return b,a*img.size/contr+b


datos = fits.getdata("../master/master_flats_normalizado.fits", 4)
vx, vy = zscale(datos)
plt.imshow(datos, vmin=vx, vmax=vy)
plt.show()
print(zscale(datos))
