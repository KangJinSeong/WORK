'''
Date: 2021.08.11
Title: Computation of power of a signal - simulation and verification
By: Kang Jin Seong
'''
from scipy.fftpack import fft, ifft, fftshift, ifftshift
import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import norm

A = 1 #Amplitude of sine wave
fc = 100 #frequemcy of sine wave
fs = 3000 # sampling frequency - oversampled by the rate of 30
nCy1 = 3 # Number of cycles of the sinewave
t = np.arange(start = 0, stop = nCy1/fc, step = 1/fs) # Time base
x = -A*np.sin(2*np.pi*fc*t) # sinusoidal function

fig, (ax1,ax2) = plt.subplots(nrows = 1, ncols = 2)
ax1.plot(t,x)
ax1.set_title('Sinusoid of frequency $f_c = 100Hz$')
ax1.set_xlabel('Time(s)');ax1.set_ylabel('Amplitude')
# fig.show()

L = len(x)
P = (norm(x)**2)/L # norm from numpy linear algo package
print('Power of the signal from time domain {:0.4f}'.format(P))

NFFT = L
X = fftshift(fft(x,NFFT))
Px = X*np.conj(X)/(L**2) # Power of each freq components
fVals = np.arange(start = -NFFT/2, stop = NFFT/2)*fs/NFFT
ax2.stem(fVals,Px,'r');ax2.set_title('Power spectral Density'); ax2.set_xlabel('Frequency (Hz)');ax2.set_ylabel('Power')
fig.show()

plt.show()