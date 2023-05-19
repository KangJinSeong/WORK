
import numpy as np # Numerical computing library

import time # Computing time measurement [debug]

from scipy import signal

import socket

import random

# Signal processing library
from scipy.signal import chirp, decimate, hilbert, find_peaks
from scipy.fftpack import fft, fftshift

from matplotlib import pyplot as plt # Plotting data [debug]

fs = 192000
t = np.arange(start = 0, stop = 0.2, step = 1/fs)
y2 = (np.zeros((1,int(0.1*fs))).tolist())[0]

exp = 10*np.exp(-10*t)
EXP = []

for i in range(len(exp)):
    data = exp[i] * random.randint(1,20)
    data = int(data)
    EXP.append(data)

result = []

result.extend(y2)
result.extend(EXP)
result.extend(y2)

while True:
    
    conn = ('30.0.1.189',9000)
    svr = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    svr.connect(conn)
    for i in range(len(result)):
        svr.send('{:3f}\n'.format(result[i]).encode())
    svr.close()
    time.sleep(0.1)
    print('send')

