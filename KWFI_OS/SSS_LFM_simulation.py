'''
Date: 2022.02.25
Title: LFM Rect Signal Simulation
By: Kang Jin Seong
'''

from weakref import ref
from scipy.fftpack import fft, ifft, fftshift, ifftshift
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import chirp, hilbert

'''
System parameter
'''
start_freq = 420e3  # start freq[kHz]
end_freq = 470e3  # end freq[kHz]
fs = end_freq * 16    # sampling frequency

Te = 0.05   # burst duration
Ne = Te*fs  # burst number of sampling
T1 = 0.005   # 1set receiving time
NT1 = T1*fs # receiving number of sampling

'''
LFM signal
'''
T = 0.1 # simulation time[sec]

N = T * fs  # number of sampling

TT = np.arange(start = 0, stop = T, step = 1/fs)

t = np.arange(start = 0, stop = Te, step = 1/fs) #Chirp time base
G1 = chirp(t, f0= start_freq, t1 = Te, f1 = end_freq, method = 'linear') # LFM Chirping Signal


RX_signal  = np.zeros((1,len(TT))).tolist()[0]
Ref = np.zeros((1,len(TT))).tolist()[0]

p = 0
for i in range(len(RX_signal)):
    if (i < Ne):
        Ref[i] = G1[i]
    else:
        Ref[i] = 0
    if ( (i <= NT1) or (i >= (NT1 + Ne)) ):
        RX_signal[i] = 0
    else:
        RX_signal[i] = G1[p]
        p += 1

Rx_result = np.array(RX_signal) + np.array(Ref)


y = signal.correlate(Rx_result,G1, method= 'fft')     # using FFT cross-correlation
y_t = np.arange(start = 0, stop = len(y))*1/fs


fig1, (axs1,axs2) = plt.subplots(nrows = 2, ncols = 1)
axs1.plot(TT, Ref,'b', label = 'first RX Signal')
axs1.plot(TT, RX_signal,'r', label = 'Second RX Signal')
axs1.set_xlabel('Time(s)');axs1.set_ylabel('Amplitude')
axs1.legend(loc = 'upper right')
axs1.set_title('rect-rect signal')
axs2.plot(y_t,y,'b')
axs2.set_title('Matched Filter-Rectangular')
axs2.set_xlabel('Time(s)')
fig1.tight_layout()
# fig1.show()

plt.show()


