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
record_time = 2 # Record time

p = pyaudio.PyAudio()
stream = p.open(format = pyaudio.paInt16, channels = 1, rate = Fs, input = True, frames_per_buffer = NumFrame)

ADC_Q = Queue()


result = []
""" Processing """
# Process0 : ADC data read

for i in range(0, int(Fs/NumFrame * record_time)):
    ADC_data = np.fromstring(stream.read(NumFrame), dtype = np.int16)/10000
    result.append(ADC_data)

stream.stop_stream()
stream.close()
p.terminate()

print('end')
result = np.array(result).flatten()
t = np.arange(start = 0, stop = len(result))*dt
plt.plot(t,result)
plt.show()
    

