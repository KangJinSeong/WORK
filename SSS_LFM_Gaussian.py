'''
Date: 2022.02.28(03.08 수정)
Title: LFM Gaussian Signal Simulation
By: Kang Jin Seong
'''


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

dr = 5      # object difference[cm]
Te = 0.001   # burst duration
Ne = Te*fs  # burst number of sampling
T1 = (dr*0.01)/1500   # 1set receiving time
NT1 = T1*fs # receiving number of sampling

'''
LFM signal
'''


T = 0.1 # simulation time[sec]

N = T * fs  # number of sampling

TT = np.arange(start = 0, stop = T, step = 1/fs)

t = np.arange(start = 0, stop = Te, step = 1/fs) #Chirp time base
G1 = chirp(t, f0= start_freq, t1 = Te, f1 = end_freq, method = 'linear') # LFM Chirping Signal
window = signal.gaussian(len(G1), std=len(G1)/5)
y1 = G1 * window

NFFT = len(y1)
A = fftshift(fft(y1, NFFT))*(1/NFFT)
f_A = np.arange(start = -NFFT/2, stop = NFFT/2)*(fs/NFFT)

RX_signal  = np.zeros((1,len(TT))).tolist()[0]
Ref = np.zeros((1,len(TT))).tolist()[0]

p = 0

for i in range(len(RX_signal)):
    if (i < Ne):
        Ref[i] = y1[i]
    else:
        Ref[i] = 0
    if ( (i <= NT1) or (i >= (NT1 + Ne)) ):
        RX_signal[i] = 0
    else:
        RX_signal[i] = y1[p]
        p += 1

Rx_result = np.array(RX_signal) + np.array(Ref)

y = signal.correlate(Rx_result,G1, method= 'fft')     # using FFT cross-correlation
y_t = np.arange(start = 0, stop = len(y))*1/fs

fig1, (axs1,axs2,axs3) = plt.subplots(nrows = 3, ncols = 1)
axs1.plot(f_A,np.abs(A))
axs1.set_xlabel('Frequency(Hz)');axs1.set_ylabel('Amplitude')
axs1.set_xlim(400e3, 500e3)
axs1.set_title('Gaussian Window')


# axs2.plot(TT, Ref,'b', label = 'first RX Signal')
# axs2.plot(TT, RX_signal,'r', label = 'Second RX Signal')
axs2.plot(TT, Rx_result,'g', label = 'Sumation RX Signal')
axs2.set_xlabel('Time(s)');axs1.set_ylabel('Amplitude')
# axs2.set_xlim(0,T1*10)
axs2.legend(loc = 'upper right')
axs2.set_title('Gaussian signal')

axs3.plot(y_t,np.real(y),'r')
axs3.set_title('Matched Filter-Gaussian')
# axs3.set_xlim(0,T1*10)
axs3.set_xlabel('Time(s)')
fig1.tight_layout()
# fig1.show()

plt.show()