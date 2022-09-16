'''
Date: 2021.10.18
Title: ADC & TDMS Write, Read
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
from nptdms import TdmsWriter, ChannelObject, TdmsFile

warnings.filterwarnings("ignore") # Ingore warning message

""" Initialize """
print("Initialize.....")

# ========== Data read ========== #
# Audio device setup
Fs = 44100# Sampling frequency
dt = 1/Fs # Sampling time
NumFrame = 4410 # Number of samples
record_time = 5 # Record time

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


with TdmsWriter("path_to_file.tdms") as tdms_writer:
    data_array = result
    channel = ChannelObject('group name', 'channel name', data_array)
    tdms_writer.write_segment([channel])

with TdmsFile.open("path_to_file.tdms") as tdms_file:
    group = tdms_file['group name']
    channel = group['channel name']
    channel_data = channel[:]   


print('end')

t = np.arange(start = 0, stop = len(channel_data))*1/Fs

t0 = np.arange(start = 0, stop = 0.128, step = 1/Fs)
coeff = chirp(t0, f0 = 0, f1 = 4000, t1 = 0.128, method = 'linear')

y = signal.correlate(channel_data, coeff, method = 'fft')
y_t = np.arange(start = 0, stop = len(y))*1/Fs


plt.figure()
plt.plot(t,channel_data)

plt.figure()
plt.psd(channel_data,len(channel_data),Fs)

plt.figure()
plt.plot(y_t,y)


plt.show()
    
