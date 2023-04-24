'''
Date: 2021.11.15
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
        
    def generate_LPF(self,q):
        NFFT = q
        f = np.arange(start = -NFFT/2, stop = NFFT/2)*(self.Fs/NFFT)
        LPF_y = np.zeros(len(f))
        LPF_y[70:130] = 2
        return LPF_y

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
        return y_c

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
        dem_y = y * np.cos(2*np.pi*self.fc*self.t)
        NFFT = len(dem_y)
        LPF_y = self.generate_LPF(NFFT)
        
        Y = fftshift(fft(dem_y,NFFT))
        f = np.arange(start = -NFFT/2, stop = NFFT/2)*(self.Fs/NFFT)
        DEM_Y = Y * LPF_y

        De_y = NFFT * ifft(ifftshift(DEM_Y),NFFT)

        fig2, (ax1, ax2,ax3,ax4) = plt.subplots(nrows = 4, ncols = 1)
        ax1.plot(f, abs(Y)/self.Fs)
        ax2.plot(f, LPF_y)
        ax3.plot(f, abs(DEM_Y))
        ax4.plot(self.t, De_y)
        plt.tight_layout()



    def mod(self):
        self.modulation_signal_DSB_SC(self.generate_traing())
        self.modulation_signal_DSB_SC(self.AWGN(self.generate_traing()))

    def demod(self):
        y_c = self.modulation_signal_DSB_SC(self.generate_traing())
        self.demodulation_signal_DSB_SC(y_c)

if __name__ == "__main__":
    print("START")
    A = Mod_DeMod()
    # A.mod()
    A.demod()
    plt.show()
