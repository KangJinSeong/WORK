
'''
Date: 2023.02.02
Title: TRX_Controller 스위칭 시험
By: Kang Jin Seong
'''

import numpy as np
from pylfsr import LFSR
import matplotlib.pyplot as plt
from scipy.signal import upfirdn
from scipy.fftpack import fft, ifft, fftshift, ifftshift
from scipy import signal
from matplotlib import font_manager, rc

font_path = "C:/Windows/Fonts/gulim.ttc"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)


class Simulator:
    def __init__(self):
        self.Rc = 5.5e3
        self.Tc = 1/self.Rc
        self.Fc = self.Rc * 4
        self.Fs = self.Fc * 4
        self.taps = [8,7,6,1]

    def Mseq_GEN(self, order, index, taps):
        inidata = np.zeros(order)
        inidata[index] = 1
        inidata = list(inidata)
        mseq = LFSR(initstate=inidata, fpoly= taps)
        cyc = 2**(order)
        tempseq = mseq.runKCycle(cyc)
        return tempseq
    def SIG_GEN(self,q,r,order, index):
        bit_t = np.arange(start = 0, stop = self.Tc * q, step = 1/self.Fs)
        bit_L = len(bit_t)
        tempseq = self.Mseq_GEN(order,index, self.taps)
        print(tempseq); print(len(tempseq))
        s_bb = upfirdn(h = [1]*bit_L, x = 2*tempseq -1 , up = bit_L)
        coef = upfirdn(h = [1]*bit_L, x = tempseq , up = bit_L)
        symbol_t = np.arange(start = 0, stop = len(s_bb))*(1/self.Fs)
        carrier = np.sin(2*np.pi*self.Rc*symbol_t)
        y = []
        for i in range(0, r):
            y.extend(s_bb * carrier)
        y = np.array(y)
        plt.subplot(1,2,1)
        plt.plot(symbol_t,s_bb, 'ro--')
        plt.plot(symbol_t, y,'go-')
        plt.grid();plt.xlabel('Time(sec)');plt.ylabel('Amplitude(V)');plt.title('Modulation Signal Generate with PN-CODE')
        plt.tight_layout()
        NFFT = len(y)
        Y = fftshift(fft(y, NFFT)*(1/NFFT))
        f = np.arange(start = -NFFT/2, stop = NFFT/2)*(self.Fs/NFFT)
        plt.subplot(1,2,2)
        plt.plot(f,abs(Y))
        plt.grid();plt.xlabel('Frequency(kHz)');plt.ylabel('Magnitude');plt.title('FFT Result')
        plt.tight_layout()      
        return  coef, y

    def main(self):
        coef, y = self.SIG_GEN(4,1,8,0)

if __name__ == "__main__":
    print('START')
    A = Simulator()
    A.main()
    plt.show()