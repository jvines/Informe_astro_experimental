from astropy.io import fits
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import scipy as sp
import numpy as np
from zscale import zscale

'''
Codigo para HDU1
'''

master_bias = fits.getdata("../master/master_bias.fits", 1)
master_flats = fits.getdata("../master/master_flats.fits", 1)

sci1 = fits.getdata("../data/dat.025.fits", 1)  # Get HDU1

sci11 = sp.divide(sci1 - master_bias, master_flats)

mn, mx = zscale(sci11)

plt.clf()
plt.imshow(sci11, vmin=mn, vmax=mx)
plt.show()

x = 453  # 232; 411
y = 1564  # 671; 1838
SR = 45  # 30
stamp = sci11[y - SR:y + SR, x - SR:x + SR]


def centroid(stamp):
    """
    Calcula el centro de la estrella viendo un centro de masasx
    con el flujo.

    Parameters
    ----------
    stamp : (N,)array_like
            Arreglo en 2-D, representa una seccion de imagen que
            engloba a una estrella.
    Returns
    -------
    cx : float
         Coordenada x del centro de la estrella.

    cy : float
         Coordenada y del centro de la estrella.
    """
    # Se crean vectores con los indices x e y de la estampilla.
    x_vect = sp.arange(0, sp.shape(stamp)[1])
    y_vect = sp.arange(0, sp.shape(stamp)[0])
    # Se estima un centro de la estrella.
    cx = sp.median(x_vect)
    cy = sp.median(y_vect)
    # Se calcula la coordenada x del centro de la estrella.
    sum_x = sp.nansum(x_vect * stamp[cy, :])
    cx = sum_x / sp.nansum(stamp[cy, :])
    # Se calcula la coordenada y del centro de la estrella.
    sum_y = sp.nansum(y_vect * stamp[:, cx])
    cy = sum_y / sp.nansum(stamp[:, cx])
    return cx, cy


def radial_profile(stamp, cy, cx):
    """
    Grafica el perfil radial de una estrella englobada dentro de stamp
    con centro en cx,cy

    Parameters
    ----------
    stamp : (N,)array_like
            Arreglo en 2-D, representa una seccion de imagen que
            engloba a una estrella.

    cx : float
         Coordenada x del centro de la estrella.

    cy : float
         Coordenada y del centro de la estrella.
    """
    x_len = sp.shape(stamp)[1]
    vect_x = sp.arange(0, x_len - int(cx))
    flux_x = stamp[int(cx):x_len, cy]
    plt.clf()
    plt.plot(vect_x, flux_x)
    plt.show()


def distance(y1, x1, y2, x2):
    return sp.sqrt((y2 - y1)**2 + (x2 - x1)**2)


def ap_phot(stamp, cy, cx, ap, sky1, sky2):
    """
    Calcula la fotometria de apertura de una estrella dentro de
    una porcion stamp de una observacion; caracterizada por un centro de
    masas cy, cx; con un radio ap; y porcion sky2 - sky1 de cielo.

    Parameters
    ----------
    stamp : (N,)array_like
            Arreglo en 2-D, representa una seccion de imagen que
            engloba a una estrella.

    cx : float
         Coordenada x del centro de la estrella.

    cy : float
         Coordenada y del centro de la estrella.

    ap : float
         Radio estimado de la estrella.

    sky1 : float
         Radio menor del anillo que representa el cielo en la imagen de la
         estrella.

    sky2 : float
         Radio mayor del anillo que representa el cielo en la imagen de la
         estrella.
    """
    x_index = sp.arange(sp.shape(stamp)[0])
    y_index = sp.arange(sp.shape(stamp)[1])
    dist = distance(y_index[cy], x_index[cx], y_index, x_index)

    star = sp.where(dist <= ap)[0]
    flux = sum(stamp[star, star])

    sky = sp.where((dist > sky1) * (dist < sky2))[0]
    sky_flux = sum(stamp[sky, sky])

    flux_f = flux - sky_flux

    return flux_f

cx, cy = centroid(stamp)
vmin, vmax = zscale(stamp)
plt.imshow(stamp, vmin=vmin, vmax=vmax)
plt.show()
radial_profile(stamp, cx, cy)
flx = ap_phot(stamp, cy, cx, 7, 20, 30)
print(flx)
