"""
Obtencion de Master Bias y Master Flats
"""

from astropy.io import fits
import scipy as sp
import matplotlib.pyplot as plt

path = "../data/dat."
"""
Esto ya lo sabemos
bias_counter = flats_counter = 0
k = 1
skipped_nums=[]

while 1:
    file = "%03d.fits" % k
    file_path = path + file
    try:
        img = fits.open(file_path)
    except IOError:
        skipped_nums.append(k)
        k += 1
        continue
    header = img[0].header['object']
    if header == 'bias':
        bias_counter += 1
    elif header == 'dome flat I Bessell':
        flats_counter += 1
    else:
        break
    k += 1
    img.close()

print("Hay {} bias y {} flats (dome flat I Bessell).".format(bias_counter,
flats_counter))
"""

biases1 = sp.array([fits.getdata("../data/dat.%03d.fits" % n, 1)
                    for n in range(1, 12)])
biases2 = sp.array([fits.getdata("../data/dat.%03d.fits" % n, 2)
                    for n in range(1, 12)])
biases3 = sp.array([fits.getdata("../data/dat.%03d.fits" % n, 3)
                    for n in range(1, 12)])
biases4 = sp.array([fits.getdata("../data/dat.%03d.fits" % n, 4)
                    for n in range(1, 12)])

header_bias0 = fits.getheader("../data/dat.001.fits", 0)
header_bias1 = fits.getheader("../data/dat.001.fits", 1)
header_bias2 = fits.getheader("../data/dat.001.fits", 2)
header_bias3 = fits.getheader("../data/dat.001.fits", 3)
header_bias4 = fits.getheader("../data/dat.001.fits", 4)

master_bias_mean1 = sp.mean(biases1, axis=0)
master_bias_mean2 = sp.mean(biases2, axis=0)
master_bias_mean3 = sp.mean(biases3, axis=0)
master_bias_mean4 = sp.mean(biases4, axis=0)

primary = fits.PrimaryHDU(header=header_bias0)
bias1 = fits.ImageHDU(data=master_bias_mean1, header=header_bias1)
bias2 = fits.ImageHDU(data=master_bias_mean2, header=header_bias2)
bias3 = fits.ImageHDU(data=master_bias_mean3, header=header_bias3)
bias4 = fits.ImageHDU(data=master_bias_mean4, header=header_bias4)
l = [primary, bias1, bias2, bias3, bias4]
hduList = fits.HDUList(l)
hduList.writeto("../master/master_bias.fits")

"""fits.setval("../master/master_bias.fits", 'BZERO',
            value=header_bias1['BZERO'], ext=1)
fits.setval("../master/master_bias.fits", 'BSCALE',
            value=header_bias1['BSCALE'], ext=1)
fits.setval("../master/master_bias.fits", 'BZERO',
            value=header_bias2['BZERO'], ext=2)
fits.setval("../master/master_bias.fits", 'BSCALE',
            value=header_bias2['BSCALE'], ext=2)
fits.setval("../master/master_bias.fits", 'BZERO',
            value=header_bias3['BZERO'], ext=3)
fits.setval("../master/master_bias.fits", 'BSCALE',
            value=header_bias3['BSCALE'], ext=3)
fits.setval("../master/master_bias.fits", 'BZERO',
            value=header_bias4['BZERO'], ext=4)
fits.setval("../master/master_bias.fits", 'BSCALE',
            value=header_bias4['BSCALE'], ext=4)"""

fits.info("../master/master_bias.fits")

###################################################

flats1 = sp.array([fits.getdata("../data/dat.%03d.fits" % n, 1)
                   for n in range(12, 13)])
flats2 = sp.array([fits.getdata("../data/dat.%03d.fits" % n, 2)
                   for n in range(12, 13)])
flats3 = sp.array([fits.getdata("../data/dat.%03d.fits" % n, 3)
                   for n in range(12, 13)])
flats4 = sp.array([fits.getdata("../data/dat.%03d.fits" % n, 4)
                   for n in range(12, 13)])

header_flats0 = fits.getheader("../data/dat.012.fits", 0)
header_flats1 = fits.getheader("../data/dat.012.fits", 1)
header_flats2 = fits.getheader("../data/dat.012.fits", 2)
header_flats3 = fits.getheader("../data/dat.012.fits", 3)
header_flats4 = fits.getheader("../data/dat.012.fits", 4)

# Primary Flats
primary = fits.PrimaryHDU(header=header_flats0)

# imageHDU1
raw_flat = sp.array([fits.getdata("../data/dat.%03d.fits" % n, 1)
                     for n in range(12, 23)])

raw_mean = sp.mean(raw_flat, axis=0)
flats = raw_mean - master_bias_mean1

mean_flats = sp.mean(flats)

flats_normalizado = sp.divide(flats, mean_flats)
master_flats_norm = sp.mean(flats_normalizado, axis=0)

flats_img1 = fits.ImageHDU(data=master_flats_norm, header=header_flats1)

# imageHDU2
raw_flat = sp.array([fits.getdata("../data/dat.%03d.fits" % n, 2)
                     for n in range(12, 23)])

raw_mean = sp.mean(raw_flat, axis=0)
flats = raw_mean - master_bias_mean2

mean_flats = sp.mean(flats)

flats_normalizado = sp.divide(flats, mean_flats)
master_flats_norm = sp.mean(flats_normalizado, axis=0)

flats_img2 = fits.ImageHDU(data=master_flats_norm, header=header_flats2)

# imageHDU3
raw_flat = sp.array([fits.getdata("../data/dat.%03d.fits" % n, 3)
                     for n in range(12, 23)])

raw_mean = sp.mean(raw_flat, axis=0)
flats = raw_mean - master_bias_mean3

mean_flats = sp.median(flats)

flats_normalizado = sp.divide(flats, mean_flats)
master_flats_norm = sp.mean(flats_normalizado, axis=0)

flats_img3 = fits.ImageHDU(data=master_flats_norm, header=header_flats3)

# imageHDU4
raw_flat = sp.array([fits.getdata("../data/dat.%03d.fits" % n, 4)
                     for n in range(12, 23)])

raw_mean = sp.mean(raw_flat, axis=0)
flats = raw_mean - master_bias_mean4

mean_flats = sp.median(flats)

flats_normalizado = sp.divide(flats, mean_flats)
master_flats_norm = sp.mean(flats_normalizado, axis=0)

flats_img4 = fits.ImageHDU(data=master_flats_norm, header=header_flats4)
l = [primary, flats_img1, flats_img2, flats_img3, flats_img4]
hduList = fits.HDUList(l)
hduList.writeto("../master/master_flats.fits")
fits.info("../master/master_flats.fits")
