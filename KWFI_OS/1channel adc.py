'''
Date: 2021.08.13
Title: Sinwave 1ADC to 8channel covolution
By: Kang Jin Seong
'''

from scipy.fftpack import fft, ifft, fftshift, ifftshift
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import chirp

fc = 32000 #frequemcy of sine wave 
fs = 192000 # sampling frequency
fs1 = 256000 # sampling frequency
fs2 = 32000*8*8 # sampling frequency
fs3 = fs2/8
nCy1 = 1000# Number of cycles of the sinewave

tt = np.arange(start = 0, stop = nCy1/fs2, step = 1/fs2)
g = chirp(tt, f0= 30000, t1 = nCy1/fs2, f1 = 34000, method = 'linear')


A = 1 #Amplitude of sine wave

t = np.arange(start = 0, stop = nCy1/fs, step = 1/fs) # time domain

t1 = np.arange(start = 0, stop = nCy1/fs1, step = 1/fs1) # time domain

t2 = np.arange(start = 0, stop = nCy1/fs2, step = 1/fs2) # time domain


x = A*np.sin(2*np.pi*fc*t) # sin wave
x1 = A*np.sin(2*np.pi*fc*t1) # sin wave
x2 = A*np.sin(2*np.pi*fc*t2) # sin wave

nCy2 = (len(x2)//8) # Number of cycles of the sinewave
# t3 = np.arange(start = 0, stop = nCy2/fs3, step = 1/fs3) # time domain
t3 = np.arange(start = 0, stop = nCy2/fs3, step = 1/fs3)
g3 = chirp(t3, f0= 30000, t1 = nCy2/fs3, f1 = 34000, method = 'linear')


x3 = A*np.sin(2*np.pi*fc*t3) # sin wave

# y1 = np.zeros((1,len(x2)))
y1 = g[0::8];y2 = g[5::8]

fig,(ax1,ax2, ax3) = plt.subplots(nrows = 3, ncols = 1)
ax1.stem(tt,g); ax1.set_title('Chirp signal Start = 30kHz, Stop = 34kHz'); ax1.set_xlabel('time(s)'); ax1.set_ylabel('Amplitude')
ax2.stem(y1);ax2.set_title('ADC channel #1'); ax2.set_xlabel('number of sample(n)'); ax2.set_ylabel('Amplitude')
ax3.stem(y2);ax3.set_title('ADC channel #5'); ax3.set_xlabel('number of sample(n)'); ax3.set_ylabel('Amplitude')
fig.tight_layout()
fig.show()


dt = 1/fs2

fig2, (ax1,ax2) = plt.subplots(nrows = 2, ncols = 1)
ax1.psd(g,len(g),fs2);ax1.set_title('Chirp signal Power Spectral density');ax1.set_xlim([0,120000])
ax2.psd(y1,len(y1),fs2/8); ax2.set_title('ADC channel #1 Power Spectral density') # plt.psd(x, NFFT, FS)
fig2.tight_layout()
fig2.show()

fig3, (ax1,ax2) = plt.subplots(nrows = 2, ncols = 1)
r1 = np.convolve(g3,y1); r2 = np.convolve(g3,y2) 
ax1.plot(r1);ax1.set_title('Convolution Result ADC channel #1'); ax1.set_xlabel('number of sample(n)'); ax1.set_ylabel('Amplitude')
ax2.plot(r2);ax2.set_title('Convolution Result ADC channel #5'); ax2.set_xlabel('number of sample(n)'); ax2.set_ylabel('Amplitude')
fig3.tight_layout()
fig3.show()




# 
# NFFT = 256
# X3 = fftshift(fft(x3,NFFT))
# Y1 = fftshift(fft(y1,NFFT))
# 
# X3_fVals = np.arange(start = -NFFT/2, stop = NFFT/2)*fs3/NFFT
# Y1_fVals = np.arange(start = -NFFT/2, stop = NFFT/2)*fs2/(NFFT*8)
# 
# fig3, (ax1,ax2) = plt.subplots(nrows = 2, ncols = 1)
# ax1.stem(X3_fVals,abs(X3));ax2.stem(Y1_fVals,abs(Y1))
# fig3.show()
