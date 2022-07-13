'''
Date: 2021.10.18
Title: TDMS Data Write & Read
By: Kang Jin Seong
'''
from scipy.fftpack import fft, ifft, fftshift, ifftshift
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import chirp
from nptdms import TdmsWriter, ChannelObject, TdmsFile
import numpy
from scipy import signal

Fs = 44100# Sampling frequency
dt = 1/Fs # Sampling time
NumFrame = 4410 # Number of samples

# with TdmsWriter("path_to_file.tdms") as tdms_writer:
#     data_array = numpy.linspace(0, 1, 10)
#     channel = ChannelObject('group name', 'channel name', data_array)
#     tdms_writer.write_segment([channel])
    

with TdmsFile.open("range 200m.test.tdms") as tdms_file:
    group = tdms_file['group name']
    channel = group['channel name']
    channel_data = channel[:]   

t = np.arange(start = 0, stop = len(channel_data))*1/Fs

# t0 = np.arange(start = 0, stop = 0.128, step = 1/Fs)
# coeff = chirp(t0, f0 = 0, f1 = 4000, t1 = 0.128, method = 'linear')

# y = signal.correlate(channel_data, coeff, method = 'fft')
# y_t = np.arange(start = 0, stop = len(y))*1/Fs


plt.figure()
plt.plot(channel_data)

# plt.figure()
# plt.psd(channel_data,len(channel_data),Fs)

# plt.figure()
# plt.plot(y_t,y)


plt.show()

