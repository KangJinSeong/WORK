'''
Date: 2021.10.15
Title: Hifiberry DAC+ADC Downsampling(singal: 30k-34kHz, Sampling: 44.1kHz)
By: Kang Jin Seong
'''

import pyaudio # Audio device interface library
import numpy as np # Numerical computing library
import pandas as pd # Data frame managing libary
import warnings # Warning message library
import time # Computing time measurement [debug]

from scipy import signal

# Signal processing library
from scipy.signal import chirp, decimate, hilbert, find_peaks
from scipy.fftpack import fft, fftshift

from multiprocessing import Queue, Process # Multiprocessing library
from matplotlib import pyplot as plt # Plotting data [debug]

warnings.filterwarnings("ignore") # Ingore warning message

""" Initialize """
print("Initialize.....")

# ========== Data read ========== #
# Audio device setup
Fs = 192000# Sampling frequency
dt = 1/Fs # Sampling time
NumFrame = 19200 # Number of samples
record_time = 1 # Record time

p = pyaudio.PyAudio()
stream = p.open(format = pyaudio.paInt16, channels = 1, rate = Fs, input = True, frames_per_buffer = NumFrame)

ADC_Q = Queue()



""" Processing """
# Process0 : ADC data read

for i in range(0, int(Fs/NumFrame * record_time)):
    ADC_data = np.fromstring(stream.read(NumFrame), dtype = np.int16)/10000
    ADC_Q.put(ADC_data)

result = []

for i in range(0, int(Fs/NumFrame * record_time)):
    ADC_data = ADC_Q.get()
    result.extend(ADC_data)

stream.stop_stream()
stream.close()
p.terminate()

print('end')
result = np.array(result)

t = np.arange(start = 0, stop = len(result))*1/Fs
NFFT = len(t)
f = np.arange(start = -NFFT/2, stop = NFFT/2)*Fs/NFFT
RESULT = fftshift(fft(result,NFFT))/NFFT

t0 = np.arange(start = 0, stop = 0.128, step = 1/Fs)
coeff = chirp(t0, f0 = 0, f1 = 4000, t1 = 0.128, method = 'linear')

y = signal.correlate(result, coeff, method = 'fft')
y_t = np.arange(start = 0, stop = len(y))*1/Fs


plt.figure()
plt.plot(t,result)

plt.figure()
plt.psd(result,len(result),Fs)

plt.figure()
plt.plot(y_t,y)


plt.show()
    
