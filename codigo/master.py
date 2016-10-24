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

print("Hay {} bias y {} flats (dome flat I Bessell).".format(bias_counter, flats_counter))
"""

fits.info("../data/dat.001.fits")

biases0 = sp.array([fits.getdata("../data/dat.%03d.fits" % n,0) for n in range(1,12)])
biases1 = sp.array([fits.getdata("../data/dat.%03d.fits" % n,1) for n in range(1,12)])
biases2 = sp.array([fits.getdata("../data/dat.%03d.fits" % n,2) for n in range(1,12)])
biases3 = sp.array([fits.getdata("../data/dat.%03d.fits" % n,3) for n in range(1,12)])
biases4 = sp.array([fits.getdata("../data/dat.%03d.fits" % n,4) for n in range(1,12)])

"""
Sabemos que funciona el master bias
"""

header_bias0=fits.getheader("../data/dat.001.fits",0)
header_bias1=fits.getheader("../data/dat.001.fits",1)
header_bias2=fits.getheader("../data/dat.001.fits",2)
header_bias3=fits.getheader("../data/dat.001.fits",3)
header_bias4=fits.getheader("../data/dat.001.fits",4)

master_bias_mean0 = sp.mean(biases0, axis=0)
master_bias_mean1 = sp.mean(biases1, axis=0)
master_bias_mean2 = sp.mean(biases2, axis=0)
master_bias_mean3 = sp.mean(biases3, axis=0)
master_bias_mean4 = sp.mean(biases4, axis=0)

fits.writeto("../master/master_bias.fits",master_bias_mean0,header=header_bias0)
fits.append("../master/master_bias.fits",master_bias_mean1,header=header_bias1)
fits.append("../master/master_bias.fits",master_bias_mean2,header=header_bias2)
fits.append("../master/master_bias.fits",master_bias_mean3,header=header_bias3)
fits.append("../master/master_bias.fits",master_bias_mean4,header=header_bias4)

fits.setval("../master/master_bias.fits", 'BZERO', value=header_bias1['BZERO'], ext=1)
fits.setval("../master/master_bias.fits", 'BSCALE', value=header_bias1['BSCALE'], ext=1)
fits.setval("../master/master_bias.fits", 'BZERO', value=header_bias2['BZERO'], ext=2 )
fits.setval("../master/master_bias.fits", 'BSCALE', value=header_bias2['BSCALE'], ext=2)
fits.setval("../master/master_bias.fits", 'BZERO', value=header_bias3['BZERO'], ext=3)
fits.setval("../master/master_bias.fits", 'BSCALE', value=header_bias3['BSCALE'], ext=3)
fits.setval("../master/master_bias.fits", 'BZERO', value=header_bias4['BZERO'], ext=4)
fits.setval("../master/master_bias.fits", 'BSCALE', value=header_bias4['BSCALE'], ext=4)

fits.info("../master/master_bias.fits")

"""
Aca termina el bias correcto
"""
"""

fits.info("../data/dat.013.fits")

flat0=fits.getdata("../data/dat.013.fits")
header0=fits.getheader("../data/dat.013.fits")

flat1 = sp.array([fits.getdata("../data/dat.%03d.fits" % n,1) for n in range(12,23)])-fits.getdata("../master/master_bias.fits",1)
flat2 = sp.array([fits.getdata("../data/dat.%03d.fits" % n,2) for n in range(12,23)])-fits.getdata("../master/master_bias.fits",2)
flat3 = sp.array([fits.getdata("../data/dat.%03d.fits" % n,3) for n in range(12,23)])-fits.getdata("../master/master_bias.fits",3)
flat4 = sp.array([fits.getdata("../data/dat.%03d.fits" % n,4) for n in range(12,23)])-fits.getdata("../master/master_bias.fits",4)

mean1=sp.mean(flat1)
mean2=sp.mean(flat2)
mean3=sp.mean(flat3)
mean4=sp.mean(flat4)

flat_norm1=flat1/mean1
flat_norm2=flat2/mean2
flat_norm3=flat3/mean3
flat_norm4=flat4/mean4

master_flat_norm1=sp.sum(flat_norm1)/11
master_flat_norm2=sp.sum(flat_norm2)/11
master_flat_norm3=sp.sum(flat_norm3)/11
master_flat_norm4=sp.sum(flat_norm4)/11

fits.writeto("../master/master_flats.fits", flat0, header=header0)
fits.append("../master/master_flats.fits", master_flat_norm1, header=fits.getheader("../data/dat.013.fits",1))
fits.append("../master/master_flats.fits", master_flat_norm2, header=fits.getheader("../data/dat.013.fits",2))
fits.append("../master/master_flats.fits", master_flat_norm3, header=fits.getheader("../data/dat.013.fits",3))
fits.append("../master/master_flats.fits", master_flat_norm4, header=fits.getheader("../data/dat.013.fits",4))

"""
master_bias_mean_data=fits.getdata("../master/master_bias.fits")

#PRIMARYHDU
raw_flat = sp.array([fits.getdata("../data/dat.%03d.fits" % n) for n in range(12,23)])
flats = raw_flat-master_bias_mean_data


header_flats=fits.getheader("../data/dat.013.fits")

mean_flats_matriz=sp.mean(flats, axis=0)
print(mean_flats_matriz.shape)
mean_flats_array=sp.median(mean_flats_matriz, axis=0)
print(mean_flats_array.shape)
master_flats_mean=sp.median(mean_flats_array, axis=0)
print(master_flats_mean.shape)
flats_normalizado=flats/master_flats_mean
master_flats_norm=sp.sum(flats_normalizado, axis=0)/11
print(master_flats_norm.shape)

fits.writeto("../master/master_flats_normalizado.fits", master_flats_norm, header=header_flats)

#imageHDU1
raw_flat = sp.array([fits.getdata("../data/dat.%03d.fits" % n,1) for n in range(12,23)])
flats = raw_flat-master_bias_mean_data

header_flats=fits.getheader("../data/dat.013.fits",1)

mean_flats_matriz=sp.mean(flats, axis=0)
print(mean_flats_matriz.shape)
mean_flats_array=sp.median(mean_flats_matriz, axis=0)
print(mean_flats_array.shape)
master_flats_mean=sp.median(mean_flats_array, axis=0)
print(master_flats_mean.shape)
flats_normalizado=flats/master_flats_mean
master_flats_norm=sp.sum(flats_normalizado, axis=0)/11
print(master_flats_norm.shape)

fits.append("../master/master_flats_normalizado.fits", master_flats_norm, header=header_flats)

#imageHDU2
raw_flat = sp.array([fits.getdata("../data/dat.%03d.fits" % n,2) for n in range(12,23)])
flats = raw_flat-master_bias_mean_data


header_flats=fits.getheader("../data/dat.013.fits",2)

mean_flats_matriz=sp.mean(flats, axis=0)
print(mean_flats_matriz.shape)
mean_flats_array=sp.median(mean_flats_matriz, axis=0)
print(mean_flats_array.shape)
master_flats_mean=sp.median(mean_flats_array, axis=0)
print(master_flats_mean.shape)
flats_normalizado=flats/master_flats_mean
master_flats_norm=sp.sum(flats_normalizado, axis=0)/11
print(master_flats_norm.shape)

fits.append("../master/master_flats_normalizado.fits", master_flats_norm, header=header_flats)

#imageHDU3
raw_flat = sp.array([fits.getdata("../data/dat.%03d.fits" % n,3) for n in range(12,23)])
flats = raw_flat-master_bias_mean_data


header_flats=fits.getheader("../data/dat.013.fits",3)

mean_flats_matriz=sp.mean(flats, axis=0)
print(mean_flats_matriz.shape)
mean_flats_array=sp.median(mean_flats_matriz, axis=0)
print(mean_flats_array.shape)
master_flats_mean=sp.median(mean_flats_array, axis=0)
print(master_flats_mean.shape)
flats_normalizado=flats/master_flats_mean
master_flats_norm=sp.sum(flats_normalizado, axis=0)/11
print(master_flats_norm.shape)

fits.append("../master/master_flats_normalizado.fits", master_flats_norm, header=header_flats)

#imageHDU4
raw_flat = sp.array([fits.getdata("../data/dat.%03d.fits" % n,4) for n in range(12,23)])
flats = raw_flat-master_bias_mean_data


header_flats=fits.getheader("../data/dat.013.fits",4)

mean_flats_matriz=sp.mean(flats, axis=0)
print(mean_flats_matriz.shape)
mean_flats_array=sp.median(mean_flats_matriz, axis=0)
print(mean_flats_array.shape)
master_flats_mean=sp.median(mean_flats_array, axis=0)
print(master_flats_mean.shape)
flats_normalizado=flats/master_flats_mean
master_flats_norm=sp.sum(flats_normalizado, axis=0)/11
print(master_flats_norm.shape)

fits.append("../master/master_flats_normalizado.fits", master_flats_norm, header=header_flats)


"""
Codigo muerto

master_bias_mean = sp.mean(biases, axis=0)


print(sp.shape(biases))

master_bias_mean = sp.mean(biases, axis=[0,1])
print(sp.shape(master_bias_mean))
fits.writeto("../master/master_bias.fits",master_bias_mean,header=header_bias)

master_bias_mean_data=fits.getdata("../master/master_bias.fits")

raw_flat = sp.array([fits.getdata("../data/dat.%03d.fits" % n) for n in range(11,23)])
flats = raw_flat-master_bias_mean_data

header_flats=fits.getheader("../data/dat.013.fits")

#"master_flats_mean = sp.mean(new_flats, axis=0)
#fits.writeto("../master/master_flats.fits",master_flats_mean,header=header_flats)


mean_ = sp.mean(flats, axis=(0,1))
print(sp.shape(mean_))
plt.plot(mean_[0])
plt.show()
#master_flats = 1./len(flats[0])*sp.divide(flats,mean_)
"""
