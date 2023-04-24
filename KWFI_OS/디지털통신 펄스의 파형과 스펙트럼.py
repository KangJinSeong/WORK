'''
Date: 2022.11.08
Title: 
By: Kang Jin Seong
'''
from scipy.fftpack import fft,fftshift
import numpy as np
import matplotlib.pyplot as plt

df = 0.01
fs = 10

t = np.arange(-5, 5, 1/fs)

signal = []
signal.extend(np.zeros(40))
signal.extend(np.ones(20))
signal.extend(np.zeros(40))
signal = np.array(signal)

NFFT = len(t)
X = fftshift(fft(signal,NFFT))
f = np.arange(start = -NFFT/2, stop = NFFT/2)*fs/NFFT

fig1, (ax1, ax2, ax3) = plt.subplots(nrows = 3, ncols = 1)
ax1.plot(t, signal)
ax2.plot(f, abs(X)/fs)
ax3.plot(f, 20*np.log10(abs(X)/fs))
plt.tight_layout()
plt.show()