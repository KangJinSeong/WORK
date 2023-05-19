
import numpy as np # Numerical computing library

import time # Computing time measurement [debug]

from scipy import signal

import socket

# Signal processing library
from scipy.signal import chirp, decimate, hilbert, find_peaks
from scipy.fftpack import fft, fftshift

from matplotlib import pyplot as plt # Plotting data [debug]

# fs = 192000

# t = np.arange(start = 0, stop = 0.1, step = 1/fs)
# t0 = np.arange(start = 0, stop = 0.1, step = 1/fs)
# y = chirp(t0, f0 = 20000, f1 = 60000, t1 = 0.1, method = 'linear')
# y2 = (np.zeros((1,int(0.05*fs))).tolist())[0]
# y3 = (np.zeros((1,int(0.001*fs))).tolist())[0]
# y4 = (np.zeros((1,int(0.049*fs))).tolist())[0]
duration = 1.0
fs = 400.0
samples = int(fs*duration)
t = np.arange(samples) / fs
signal = chirp(t, 20.0, t[-1], 100.0)
signal *= (1.0 + 0.5 * np.sin(2.0*np.pi*3.0*t) )
analytic_signal = hilbert(signal)
amplitude_envelope = np.abs(analytic_signal)

plt.figure()
plt.plot(amplitude_envelope)
plt.show()

# 
# rx = []
# rx.extend(y2)
# rx.extend(y)
# rx.extend(y2)
# 
# 
# rx1 = []
# rx1.extend(y2)
# rx1.extend(y3)
# rx1.extend(0.7*y)
# rx1.extend(y4)
# 
# y5 = (np.zeros((1,int(0.002*fs))).tolist())[0]
# y6 = (np.zeros((1,int(0.048*fs))).tolist())[0]
# 
# rx2 = []
# rx2.extend(y2)
# rx2.extend(y5)
# rx2.extend(0.5*y)
# rx2.extend(y6)
# 
# y7 = (np.zeros((1,int(0.003*fs))).tolist())[0]
# y8 = (np.zeros((1,int(0.047*fs))).tolist())[0]
# 
# rx3 = []
# rx3.extend(y2)
# rx3.extend(y7)
# rx3.extend(0.3*y)
# rx3.extend(y8)
# 
# y9 = (np.zeros((1,int(0.004*fs))).tolist())[0]
# y10 = (np.zeros((1,int(0.046*fs))).tolist())[0]
# 
# rx4 = []
# rx4.extend(y2)
# rx4.extend(y9)
# rx4.extend(0.4*y)
# rx4.extend(y10)
# 
# RX = np.array(rx) + np.array(rx1) + np.array(rx2) + np.array(rx3) + np.array(rx4)
# 
# result = signal.correlate(RX, y, method = 'fft')

# result = abs(result)
# result = result / max(result)
# plt.figure()
# plt.plot(RX)
# 
# plt.figure()
# plt.plot(result)
# plt.show()

while True:
    
    conn = ('30.0.1.189',9000)
    svr = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    svr.connect(conn)
    for i in range(len(result)):
        svr.send('{:3f}\n'.format(result[i]).encode())
    svr.close()
    time.sleep(0.1)
    print('send')
