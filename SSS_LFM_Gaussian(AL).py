'''
Date: 2022.03.08
Title: LFM Rect Signal Simulation
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

Te = 0.001   # burst duration
Ne = Te*fs  # burst number of sampling
T1 = 0.005  # 1set receiving time
NT1 = T1*fs # receiving number of sampling

dr = 5 # object difference[cm]

'''
LFM signal
'''

K = (end_freq - start_freq) / Te   # chirping rate
s = 0.35

T2 = T1 + (dr*0.01)/750     # T2 시간 계산 dr 길이 [m]변환
T = T2 + (Te*10)
N = int(T*fs)

dR = (T2-T1)*750    #최종 길이
TT = np.zeros((1,N)).tolist()[0]
y1 = np.zeros((1,N)).tolist()[0]
y2 = np.zeros((1,N)).tolist()[0]

y = np.zeros((1,N)).tolist()[0]
Ref = np.zeros((1,N)).tolist()[0]

for i in range(1,N+1):
    t = i/fs
    TT[i-1] = t*750*100   # time data
    if (t < T1) or (t > T1+Te):
        y1[i-1] = 0
    else:
        y1[i-1] = np.exp(pow((t-(T1+Te/2)) / (s*(Te/2)),2)*(-0.5)) * np.sin(2*np.pi*( (K/2)*pow(t-T1,2) + start_freq*(t-T1) ))
    if (t < T2) or (t > T2+Te):
        y2[i-1] = 0
    else:
        y2[i-1] = np.exp(pow((t-(T2+Te/2)) / (s*(Te/2)),2)*(-0.5)) * np.sin(2*np.pi*( (K/2)*pow(t-T2,2) + start_freq*(t-T2) ))
    y[i-1] = y1[i-1] + y2[i-1]

    Ref[i-1] = np.exp(pow((t-(Te/2)) / (s*(Te/2)),2)*(-0.5)) * np.sin(2*np.pi*( (K/2)*pow(t,2) + start_freq*(t) ))


Result = signal.correlate(y,Ref, method= 'fft')     # using FFT cross-correlation
Result_t = np.arange(start = 0, stop = len(Result))*1/fs

NFFT = len(y1)
A = fftshift(fft(y1, NFFT))*(1/NFFT)
f_A = np.arange(start = -NFFT/2, stop = NFFT/2)*(fs/NFFT)



fig1, (axs1,axs2,axs3) = plt.subplots(nrows = 3, ncols = 1)
axs1.plot(f_A,np.abs(A))
axs1.set_xlabel('Frequency(Hz)');axs1.set_ylabel('Amplitude')
axs1.set_xlim(400e3, 500e3)
axs1.set_title('Gaussian Window')


axs2.plot(TT, Ref,'b', label = 'first RX Signal')
axs2.plot(TT, y,'r', label = 'Second RX Signal')
axs2.set_xlabel('distance(cm)');axs1.set_ylabel('Amplitude')
axs2.legend(loc = 'upper right')
axs2.set_title('Gaussian signal')

axs3.plot(Result_t,np.real(Result),'b')
axs3.set_title('Matched Filter-Gaussian')
axs3.set_xlabel('Time(s)')
fig1.tight_layout()
# fig1.show()

plt.show()

