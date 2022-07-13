#%%
'''
Date: 2021.10.14
Title: Bandpass sampleing theory test( ADC:10kHZ simulation)
By: Kang Jin Seong
'''
import time
from scipy.fftpack import fft, fftshift
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import chirp, hilbert
from scipy import signal

'''
Demo Data Generate: 30kHz
'''
fs = 100000 # sampling frequency
s_t = np.arange(start = 0, stop = 0.001, step = 1/fs) # time base vector
sum_sig = np.cos(2*np.pi*30000*s_t) # signal vector

d_t = np.arange(start = 0, stop = 0.1, step = 1/fs) # delay time base vector
a = (np.zeros((1,len(d_t))).tolist())[0]

# Demo Data generate
sig = []
sig.extend(a)
sig.extend(sum_sig)
sig.extend(a)
sig = np.array(sig)
print(type(sig))

sig_t = np.arange(start = 0, stop = len(sig)/fs, step = 1/fs)

'''
Demo Data FFT
'''
NFFT = len(sig_t) # FFT window size
SIG = fftshift(fft(sig,NFFT))/NFFT
f = np.arange(start = -NFFT/2, stop = NFFT/2)*fs/NFFT   # frequency base vector

'''
ADC System signal Train generate
'''

sample_t = np.arange(start = 0, stop = 0.0001, step = 1/fs)
b = (np.zeros((1,len(sample_t))).tolist())[0]
b[len(b)-1] = 1

sample_sig = []
for i in range(0,2010):
    sample_sig.extend(b)
print(len(sample_sig))
print(sample_sig[0])

sample_sig_t = np.arange(start = 0, stop = len(sample_sig)/fs, step = 1/fs)
NFFT1 = len(sample_sig_t)


SAMPLE_SIG = fft(sample_sig,NFFT1)/NFFT1
f1 = np.arange(start = 0, stop = NFFT1)*fs/NFFT1


'''
Result Data is convolution data at Frequency domain with Demo data & ADC system
'''
result = signal.fftconvolve(SIG, SAMPLE_SIG, mode = 'full')
f2 = np.arange(start = (-NFFT1)+1, stop = (NFFT1))*fs/NFFT1

fig1, axs = plt.subplots(nrows = 2, ncols = 2)
axs[0,0].plot(sig_t, sig);axs[0,0].set_title('Demo data(30kHz, sine wave)'); axs[0,0].set_xlabel('Time(sec)'); axs[0,0].set_ylabel('Amplitude')
axs[0,1].plot(f,abs(SIG));axs[0,1].set_title('Demo data(FFT signal)'); axs[0,1].set_xlabel('Frequency(Hz)'); axs[0,1].set_ylabel('Amplitude')
axs[1,0].stem(sample_sig_t,sample_sig);axs[1,0].set_xlim([0,0.0008]);axs[1,0].set_title('ADC System(sec)'); axs[1,0].set_xlabel('Time(sec)'); axs[1,0].set_ylabel('Amplitude')
axs[1,1].plot(f1, abs(SAMPLE_SIG));axs[1,1].set_title('ADC System(FFT signal)'); axs[1,1].set_xlabel('Frequency(Hz)'); axs[1,1].set_ylabel('Amplitude')

fig1.tight_layout()
fig1.show()
# fig1.savefig(r'C:\Users\USER\Desktop\DSP_python\figure\Downsampling with ADC System simulation.png',dpi = 300)

plt.figure()
plt.plot(f2,result);plt.title('Convolution Data result'); plt.xlabel('Frequency(Hz)'); plt.ylabel('Amplitude')
# plt.savefig(r'C:\Users\USER\Desktop\DSP_python\figure\ADC System Convolution Result.png',dpi = 300)

plt.figure()
plt.plot(f2,result);plt.xlim([5000,15000]);plt.title('Convolution Data result'); plt.xlabel('Frequency(Hz)'); plt.ylabel('Amplitude')
# plt.savefig(r'C:\Users\USER\Desktop\DSP_python\figure\ADC System Convolution Result(10kHz).png',dpi = 300)




plt.show()

# %%
