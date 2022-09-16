'''
Date: 2022.01.07
Title: Side Scan Sonar_V1.0
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


class SSS:
    def __init__(self,Fs,NumFrame,record_time):
        self.Fs = Fs
        self.NF = NumFrame
        self.RX_time = record_time
        self.ADC_Q = Queue()
    def ADC(self):
        p = pyaudio.PyAudio()
        stream = p.open(format = pyaudio.paInt16, channels = 1, rate = self.Fs, input = True, frames_per_buffer = self.NF)
    
        for i in range(0, int(self.Fs/self.NF * self.RX_time)):
#             ADC_data = np.fromstring(stream.read(self.NF), dtype = np.int16)/10000
            ADC_data = np.fromstring(stream.read(self.NF), dtype = np.int16)
            self.ADC_Q.put(ADC_data)

        stream.stop_stream()
        stream.close()
        p.terminate()
        
        result = []

        for i in range(0, int(self.Fs/self.NF * self.RX_time)):
            ADC_data = self.ADC_Q.get()
            result.extend(ADC_data)
        
        t = np.arange(start = 0, stop = len(result))*(1/self.Fs)
        plt.figure()
        plt.stem(t[0:1000],result[0:1000])
#         plt.xlim(0.0005,0.0007)
        
    def PWM(self):
        pass
    
    
    def main(self):
        self.ADC()
    

if __name__ == "__main__":
    plt.close()
    result = SSS(192000,19200,0.2)    #SSS(Fs,NumFrame,record_time)
    result.main()
    plt.show()
