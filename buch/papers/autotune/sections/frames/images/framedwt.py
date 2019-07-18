"""
Created on Tue May  7 14:28:53 2019

@author: Cedric


Plot the  set of 1D demo signals available in `pywt.data.demo_signal`.
"""

import numpy as np
import matplotlib.pyplot as plt
import pywt
from scipy.signal import chirp
from scipy.interpolate import interp1d
import scipy
import scipy.ndimage as ndimage
import scipy.ndimage.filters as filters
from skimage.feature import peak_local_max

neighborhood_size = 5
threshold = 1500

t = []
sig = []
wlen = []
coff = []
coff2 = []
coffap = []
samp = 4096*2
nr = 48
fs = []
freq = []
for x in range(13):
    freq.append(int(220*np.power(np.power(2, 1/12), x)))

fi = np.zeros(1000)
tx = np.linspace(0, 1, 10000)
t1 = np.linspace(0, 0.1, 1000)
sig1 = (-0.5*np.cos(20*np.pi*t1)+0.5)*np.sin(freq[0]*np.pi*t1)
t2 = np.linspace(0.3, 0.4, 1000)
sig2 = (-0.5*np.cos(20*np.pi*t2)+0.5)*np.sin(freq[1]*2*np.pi*t2)
t3 = np.linspace(0.4, 0.5, 1000)
sig3 = (-0.5*np.cos(20*np.pi*t3)+0.5)*np.sin(freq[2]*2*np.pi*t3)
t4 = np.linspace(0.6, 0.7, 1000)
sig4 = (-0.5*np.cos(10*np.pi*t4)+0.5)*np.sin(freq[2]*2*np.pi*t4)
t5 = np.linspace(0.7, 0.8, 1000)
sig5 = np.sin(freq[5]*2*np.pi*t5)
t6 = np.linspace(0.8, 0.9, 1000)
sig6 = np.sin(freq[6]*2*np.pi*t6)
t7 = np.linspace(0.9, 1, 1000)
sig7 = (0.5*np.cos(10*np.pi*t4)+0.5)*np.sin(freq[6]*2*np.pi*t4)
sigx = np.concatenate((sig1, sig1, fi, sig2, sig3, fi, sig4, sig5, sig6, sig7))


plt.figure(figsize=(8, 3))
#plt.text(0.1, -1, r'$110[Hz]$',
#         {'color': 'black', 'fontsize': 12, 'ha': 'center', 'va': 'center',
#          'bbox': dict(boxstyle="round", fc="white", ec="black", pad=0.2)})



for x in range(nr):
    fs.append(int(samp*np.power(np.power(2, 1/nr), x)))
    t.append(np.linspace(0, 1, fs[x]))
    #Testsignale

    #Stetiger Sinus 220Hz
    #sig.append(np.sin(220*2*np.pi*t[x]))

    #Sinus * arctan
    #sig.append(np.arctan(t[x])*np.sin(220*np.pi*t[x]))

    #Cos anstieg mit

    #sig.append((-0.5*np.cos(6*np.pi*t[x])+0.5)*np.sin(220*np.pi*t[x]))

for x in range(nr):
    #testsig
    #sig.append(testsig(fs[x]))
    # Stetiger Frequenzsweep 100-200Hz
    #sig.append(chirp(t[x], 100, 2, 200, 'linear'))
    #sig.append((-0.5*np.cos(6*np.pi*t[x])+0.5)*chirp(t[x], 20, 2, 400, 'linear'))
    sig.append(np.interp(t[x], tx, sigx))
    wlen.append(pywt.dwt_max_level(len(sig[x]), 'db8'))
    coff.append(pywt.wavedec(sig[x], 'db8', level=min(wlen)))

#x = np.linspace(0, 2*np.pi, 10)
#y = np.sin(x)
#xvals = np.linspace(0, 2*np.pi, 50)



plt.plot(t[-1], sig[-1])
plt.savefig('testsig.jpg', dpi=1200)
plt.figure()

sampling_period = 1 / fs[0]
coef, freqs = pywt.cwt(sig[0], np.arange(1, 254), 'cgau8',
                       sampling_period=sampling_period)
coef = np.abs(coef)
cs = plt.contourf(t[0], freqs, coef, 200, cmap=plt.cm.gnuplot2)
plt.ylim([20, 600])
cbar = plt.colorbar(cs)
plt.xlabel('Zeit in [s]')
plt.ylabel('Frequenz in [Hz]')
plt.savefig('sincosmcwt.jpg',dpi=1200)
print(min(wlen))
#for m in range(len(t)):
#    print(len(t[m]))

for r in range(len(coff)):
    coff2.append([])
    tp = np.linspace(0, 1, len(coff[r][-1]))
    for k in range(len(coff[r])-1):
        tp = np.linspace(0, 1, len(coff[r][k]))
        co = interp1d(tp, coff[r][k], kind='quadratic')
        #co = interp1d(tp, coff[r][k], kind='next')
        coff2[r].append(co(t[-1]))

#for r in range(len(coff2)):
#    for k in range(len(coff2[r])):
#        plt.plot(t[-1], coff2[r][k])

arr = np.asarray(coff2)
print(arr.shape)
for k in range(min(wlen)):
    for r in range(len(coff2)):
        coffap.append(coff2[r][k])


plt.figure()
level = samp/np.power(2, min(wlen))/2
laen = []
for q in range(min(wlen)):
    level1 = np.power(2, q)*level
    level2 = np.power(2, q+1)*level
    laen.append(np.linspace(level1, level2, nr))


#laen = np.linspace(0, 1, len(coffap))
figsize=(40, 10)
hoeh = np.linspace(0, 1, len(coffap[-1]))
X, Y = np.meshgrid(hoeh, laen)
print(X.shape)
coffap = np.abs(coffap)
cs = plt.contourf(X,Y,coffap,400,cmap=plt.cm.gnuplot2)
cbar = plt.colorbar(cs)
#cbar.ax.set_ylabel('verbosity coefficient')
#plt.pcolor(coffap)
#plt.title('Sinus 220Hz')
plt.xlabel('Zeit in [s]')
plt.ylabel('Frequenz in [Hz]')
plt.ylim([20, 600])

#plt.savefig('sincos.pdf')
plt.savefig('sincosmdwt.jpg',dpi=1200)

#grid_z0 = griddata(points, values, (X, Y), method='nearest')
#grid_z1 = griddata(points, values, (grid_x, grid_y), method='linear')
#grid_z2 = griddata(points, values, (grid_x, grid_y), method='cubic')


"""
plt.figure()

data_max = filters.maximum_filter(coffap, neighborhood_size)
maxima = (coffap == data_max)
data_min = filters.minimum_filter(coffap, neighborhood_size)
diff = ((data_max - data_min) > threshold)
maxima[diff == 0] = 0

labeled, num_objects = ndimage.label(maxima)
slices = ndimage.find_objects(labeled)
x, y = [], []
for dy,dx in slices:
    x_center = (dx.start + dx.stop - 1)/2
    x.append(x_center)
    y_center = (dy.start + dy.stop - 1)/2
    y.append(y_center)

plt.imshow(coffap)
plt.savefig('data.png', bbox_inches = 'tight')

plt.autoscale(False)
plt.plot(x,y, 'ro')
plt.savefig('result.png', bbox_inches = 'tight')


#xy = peak_local_max(coffap, min_distance=2,threshold_abs=1500)
"""
