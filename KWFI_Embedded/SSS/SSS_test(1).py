'''
Date: 2022.01.05
Title: Side Scan Sonar test(1)
By: Kang Jin Seong
'''

import pyaudio # Audio device interface library
import numpy as np # Numerical computing library
import pandas as pd # Data frame managing libary
import warnings # Warning message library
import time # Computing time measurement [debug]

from scipy import signal

import RPi.GPIO as GPIO
import pigpio
import socket

# Signal processing library
from scipy.signal import chirp, decimate, hilbert, find_peaks
from scipy.fftpack import fft, fftshift

from multiprocessing import Queue, Process # Multiprocessing library
from matplotlib import pyplot as plt # Plotting data [debug]

warnings.filterwarnings("ignore") # Ingore warning message

""" Initialize """
# print("Initialize.....")

# ========== Data read ========== #
# Audio device setup
Fs = 192000# Sampling frequency
dt = 1/Fs # Sampling time
NumFrame = 1920 # Number of samples
record_time = 0.2 # Record time



ADC_Q = Queue()


# PI = pigpio.pi()

X = 0
while X < 1000:
    X += 1
    PI = pigpio.pi()    
    t = 1/10000

    f = 430000
    TX_start = time.time()
    for i in range(100):
        PI.hardware_PWM(13,f,500000)
        f += 400
        time.sleep(t)
        
    PI.hardware_PWM(13,0,500000)
    PI.stop()
    TX_end = time.time()

    p = pyaudio.PyAudio()
    stream = p.open(format = pyaudio.paInt16, channels = 1, rate = Fs, input = True, frames_per_buffer = NumFrame)
    

    """ Processing """
    # Process0 : ADC data read
    RX_start = time.time()
    for i in range(0, int(Fs/NumFrame * record_time)):
        ADC_data = np.fromstring(stream.read(NumFrame), dtype = np.int16)/10000
        ADC_Q.put(ADC_data)
        
    stream.stop_stream()
    stream.close()
#     p.terminate()

    RX_end = time.time()

    DSP_start = time.time()
    result = []

    for i in range(0, int(Fs/NumFrame * record_time)):
        ADC_data = ADC_Q.get()
        result.extend(ADC_data)


    # print('end')
    result = np.array(result)
    t0 = np.arange(start = 0, stop = 0.01, step = 1/Fs)
    coeff = chirp(t0, f0 = 1000, f1 = 21000, t1 = 0.01, method = 'linear')

    y = signal.correlate(result, coeff, method = 'fft')
#     y_max = np.max(abs(y))
#     y = abs(y)/y_max
    y = y.tolist()
    print(len(y))
    plt.plot(y)
    plt.show()
#     DSP_end = time.time()
# 
#     ETH_start = time.time()
#     conn = ('30.0.1.187',9000)
#     svr = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#     svr.connect(conn)
#     for i in range(len(y)):
#     #     print(i)
#         svr.send('{:3f}\n'.format(y[i]).encode())
#     #     data = svr.recv(1024).decode()
#     svr.close()    
#     ETH_end = time.time()
# 
# 
#     print('TX Time:', TX_end-TX_start)
#     print('RX Time:', RX_end-RX_start)
#     print('DSP Time:', DSP_end-DSP_start)
#     print('ETH Time:', ETH_end-ETH_start)

