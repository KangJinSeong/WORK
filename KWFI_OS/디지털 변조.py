'''
Date: 2022.11.28
Title: 
By: Kang Jin Seong
'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import upfirdn

class MOD:
    def __init__(self):
        self.L = 1000
        self.Fs = 20*self.L
        self.Ts = 1/self.Fs
        self.fc = 5e3
        self.fc2 = 2e3
        self.b = [1,0,0,1,0,1]
    def OOK(self):
        b = np.array(self.b)
        L = int(1e-3*self.Fs)
        ask_s_bb = upfirdn(h = [1]*L, x = b, up = L)
        t = np.arange(start = 0, stop = 6e-3, step=self.Ts)
        y = np.cos(2*np.pi*self.fc*t) * ask_s_bb
        # print(len(t), len(ask_s_bb))
        fig1, (ax1, ax2,ax3,ax4) = plt.subplots(nrows = 4, ncols = 1)
        ax1.plot(t,ask_s_bb);ax1.grid()
        ax2.plot(t, y);ax2.grid()
        ax3.psd(ask_s_bb, len(ask_s_bb), self.Fs)
        ax4.psd(y,len(y), self.Fs)
        plt.tight_layout()

    def FSK(self):
        b = np.array(self.b)
        L = int(1e-3*self.Fs)
        fsk1_s_bb = upfirdn(h = [1]*L, x = b, up = L)
        fsk2_s_bb = upfirdn(h = [1]*L, x = -b+1, up = L)
        fsk_s_bb = fsk1_s_bb - fsk2_s_bb
        t = np.arange(start = 0, stop = 6e-3, step=self.Ts)
        y1 = np.sin(2*np.pi*self.fc*t) * fsk1_s_bb
        y2 = np.sin(2*np.pi*self.fc2*t) * fsk2_s_bb
        y = y1 + y2
        fig1, (ax1, ax2,ax3,ax4) = plt.subplots(nrows = 4, ncols = 1)
        ax1.plot(t,fsk_s_bb);ax1.grid()
        ax2.plot(t, y);ax2.grid()
        ax3.psd(fsk_s_bb, len(fsk_s_bb), self.Fs)
        ax4.psd(y,len(y), self.Fs)
        plt.tight_layout()  

    def PSK(self):
        b = np.array(self.b)
        L = int(1e-3*self.Fs)
        psk_s_bb = upfirdn(h = [1]*L, x = 2*b-1, up = L)
        t = np.arange(start = 0, stop = 6e-3, step=self.Ts)
        y = np.sin(2*np.pi*self.fc*t) * psk_s_bb
        # print(len(t), len(ask_s_bb))
        fig1, (ax1, ax2,ax3,ax4) = plt.subplots(nrows = 4, ncols = 1)
        ax1.plot(t,psk_s_bb);ax1.grid()
        ax2.plot(t, y);ax2.grid()
        ax3.psd(psk_s_bb, len(psk_s_bb), self.Fs)
        ax4.psd(y,len(y), self.Fs)
        plt.tight_layout()

    def main(self):
        # self.OOK()
        # self.FSK()
        self.PSK()

if __name__ == "__main__":
    print("START")
    A = MOD()
    A.main()
    plt.show()
