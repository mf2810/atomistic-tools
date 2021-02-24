import numpy as np
import pylab as plb
import matplotlib.pyplot as plt
import scipy
from scipy.optimize import curve_fit
from scipy import asarray as ar,exp
import sys

print('welcome')
T = 400
bonds = True
bonds = False
k = np.loadtxt('hist.xvg')

##############################################

for i in range(0, len(k)):
    k[i,1] = k[i,1]/np.sin(np.radians(k[i,0]))

sumk = np.sum(k[:,1])
for i in range(0, len(k)):
    k[i,1] = k[i,1]/sumk

x = ar(k[:,0])
y = ar(k[:,1])

n = len(x)                          #the number of data
mean = sum(x*y)/n                   #note this correction
sigma = sum(y*(x-mean)**2)/n        #note this correction

def gaussian(x, height, center, width, offset):
    return height*np.exp(-(x - center)**2/(2*width**2)) + offset

def three_gaussians(x, h1, c1, w1, h2, c2, w2, h3, c3, w3, offset):
#    offset = 0
    return (gaussian(x, h1, c1, w1, offset=0) +
        gaussian(x, h2, c2, w2, offset=0) +
        gaussian(x, h3, c3, w3, offset=0))

def two_gaussians(x, h1, c1, w1, h2, c2, w2, offset):
    return three_gaussians(x, h1, c1, w1, h2, c2, w2, 0,0,1, offset=0)

def one_gaussians(x, h1, c1, w1, offset):
    return three_gaussians(x, h1, c1, w1,0,0,1,0,0,1, offset=0)

errfunc1 = lambda p, x, y: (one_gaussians(x, *p) - y)**2

guess1 = [sum(y)/n, sum(x)/n, sigma, 0]  # I removed the peak I'm not too sure about
optim1, success = scipy.optimize.leastsq(errfunc1, guess1[:], args=(x, y))

if bonds == False:
    print('\n\n')
    print('theta_0 [degrees],k_theta [kJ mol-1 rad-2]')
    print('%.2f\t%.4f' %(optim1[1], (8.3144598/1000)*(T/optim1[2]**2) * (180**2)/(np.pi)**2))
else:
    print('\n\n')
    print('b_0 [nm] ,k_b [kJ mol-1 nm-2]')
    print(optim1[1], (8.3144598/1000)*(T/optim1[2]**2))

plt.plot(x, y, lw=5, c='g', label='measurement')
plt.scatter(x, one_gaussians(x, *optim1),
    lw=1, c='g', label='fit of 1 Gaussians')
plt.legend(loc='best')
plt.savefig('result.png')
plt.show()


