'''
Date: 2021.11.10
Title: 
By: Kang Jin Seong
'''

from scipy.fftpack import fft, ifft, fftshift, ifftshift
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal


class Mod_DeMod:
    def __init__(self):
        self.T = 1e-3
        self.Fs = 1/self.T
        self.fc = 250
        self.t = np.arange(-0.1,0.1,self.T)

    def generate_traing(self):
        y = np.zeros(len(self.t))
        y[50:150] = signal.triang(100)
        return y

    def modulation_signal_DSB_SC(self,y):
        y_c = y * np.cos(2*np.pi*self.fc*self.t)

        NFFT = len(y)
        Y = fftshift(fft(y,NFFT))
        Y_C = fftshift(fft(y_c,NFFT))
        f = np.arange(start = -NFFT/2, stop = NFFT/2)*(self.Fs/NFFT)

        fig1, (ax1, ax2,ax3,ax4) = plt.subplots(nrows = 4, ncols = 1)
        ax1.plot(self.t, y)
        ax2.plot(self.t, y_c)
        ax3.plot(f,abs(Y)/self.Fs)
        ax4.plot(f,abs(Y_C)/self.Fs)
        plt.tight_layout()

    def AWGN(self,y):
        snr_dB = 6           #SNR in dB
        snr = pow(10,snr_dB/10)    #linear SNR
        signal_power = pow(np.linalg.norm(y),2)/len(y)    #modulated signal power(신호벡터크기 계산)
        noise_power = signal_power/snr  #noise power
        noise_std = np.sqrt(noise_power)    #noise standard deviation
        noise = noise_std*np.random.normal(size = (len(y))) # awgn noise
        rx_signal = y+noise
        return rx_signal

    def demodulation_signal_DSB_SC(self,y):
        rx_y = y * np.cos(2*np.pi*self.fc*self.t)

    def mod(self):
        self.modulation_signal_DSB_SC(self.generate_traing())
        self.modulation_signal_DSB_SC(self.AWGN(self.generate_traing()))

    def demod(self):
        pass

if __name__ == "__main__":
    print("START")
    A = Mod_DeMod()
    A.mod()
    plt.show()


