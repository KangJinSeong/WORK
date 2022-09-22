'''
Date: 2022.03.08
Title: LFM Hetrodyne Signal Simulation
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
carrier_freq = 420e3
fs = end_freq * 16    # sampling frequency

dr = 50      # object difference[cm]
Te = 0.001   # burst duration
Ne = Te*fs  # burst number of sampling
T1 = (dr*0.01)/750   # 1set receiving time
NT1 = T1*fs # receiving number of sampling

de_fs = 80e3

'''
LFM signal
'''

T = 0.1 # simulation time[sec]

t = np.arange(start = 0, stop = Te, step = 1/fs) #Chirp time base
G1 = chirp(t, f0= start_freq, t1 = Te, f1 = end_freq, method = 'linear') # LFM Chirping Signal
window = signal.gaussian(len(G1), std=len(G1)/5)
y1 = G1 * window
c_c = np.cos(2*np.pi*carrier_freq*t)
pre_signal = y1 * c_c


de_rate = int(fs/de_fs)


pre_result = signal.decimate(pre_signal, de_rate, ftype='fir')

plt.figure()
plt.subplot(3,1,1)
plt.psd(y1,512,fs);plt.xlabel('Frequency[Hz]'); plt.title('RX Signal')

plt.subplot(3,1,2)
plt.psd(pre_signal,512,fs);plt.xlabel('Frequency[Hz]'); plt.title('Modulated Signal')

plt.subplot(3,1,3)
plt.psd(pre_result,len(pre_result),de_fs);plt.xlabel('Frequency[Hz]'); plt.title('Decimated Signal')
plt.tight_layout()

TT = np.arange(start = 0, stop = T, step = 1/de_fs)
de_Ne = Te*de_fs  # burst number of sampling(Decimate)
de_NT1 = T1*de_fs # receiving number of sampling(Decimate)
de_t = np.arange(start = 0, stop = Te, step = 1/de_fs) #Chirp time base
de_start_freq = 0  # start freq_decimate[kHz]
de_end_freq = 40e3  # end freq_decimate[kHz]

de_G1 = chirp(de_t, f0= de_start_freq, t1 = Te, f1 = de_end_freq, method = 'linear') # LFM Chirping Signal


RX_signal  = np.zeros((1,len(TT))).tolist()[0]
Ref = np.zeros((1,len(TT))).tolist()[0]

p = 0

for i in range(len(RX_signal)):
    if (i < de_Ne):
        Ref[i] = pre_result[i]
    else:
        Ref[i] = 0
    if ( (i <= de_NT1) or (i >= (de_NT1 + de_Ne)) ):
        RX_signal[i] = 0
    else:
        RX_signal[i] = pre_result[p]
        p += 1

Rx_result = np.array(RX_signal) + np.array(Ref)

y = signal.correlate(Rx_result,de_G1, method= 'fft')     # using FFT cross-correlation
y_t = np.arange(start = 0, stop = len(y))*1/de_fs

fig1, (axs2,axs3) = plt.subplots(nrows = 2, ncols = 1)

# axs2.plot(TT, Ref,'b', label = 'first RX Signal')
# axs2.plot(TT, RX_signal,'r', label = 'Second RX Signal')
axs2.plot(TT, Rx_result,'g', label = 'Sumation RX Signal')
axs2.set_xlabel('Time(s)');axs2.set_ylabel('Amplitude')
axs2.set_xlim(0,T1*10)
axs2.legend(loc = 'upper right')
axs2.set_title('Gaussian signal')

axs3.plot(y_t,np.real(y),'r')
axs3.set_title('Matched Filter-Gaussian')
axs3.set_xlim(0,T1*10)
axs3.set_xlabel('Time(s)')
fig1.tight_layout()
# fig1.show()

plt.show()