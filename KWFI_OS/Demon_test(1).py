'''
Date: 2022.02.25
Title: Sonar DEMON Algorithum test
By: Kang Jin Seong
'''

from cmath import log10
from scipy.fftpack import fft, ifft, fftshift, ifftshift
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

Fs = 192e3
t = np.arange(start = 0, stop = 10, step = 1/Fs)

Rx_signal = np.cos(2*np.pi*50*t) + np.cos(2*np.pi*115*t) + np.cos(2*np.pi*230*t) + np.cos(2*np.pi*400*t) + np.cos(2*np.pi*900*t)

snr_dB = 10            #SNR in dB
snr = pow(10,snr_dB/10)    #linear SNR
signal_power = pow(np.linalg.norm(Rx_signal),2)/len(Rx_signal)    #modulated signal power(신호벡터크기 계산)
noise_power = signal_power/snr  #noise power
noise_std = np.sqrt(noise_power)    #noise standard deviation
noise = noise_std*np.random.normal(size = (len(Rx_signal))) # awgn noise

RX_result = noise + Rx_signal



