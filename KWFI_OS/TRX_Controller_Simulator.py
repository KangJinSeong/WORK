'''
Date: 2023.02.07(rev1.1)
Title: 3차원 해수유동 TRX_Controller_Simulator TDMS 생성 코드
By: Kang Jin Seong
'''

from nptdms import TdmsWriter, ChannelObject, TdmsFile
import numpy as np
from pylfsr import LFSR
import matplotlib.pyplot as plt
from scipy.signal import upfirdn
from scipy.fftpack import fft, ifft, fftshift, ifftshift
from scipy import signal

class Simulator:
    def __init__(self):
        self.Rc = 5.5e3
        self.Tc = 1/self.Rc
        self.Fc = self.Rc * 4
        self.Fs = self.Fc * 10

        self.taps = [8,7,6,1]   # 8order
        # self.taps = [6,8,11,12] # 12order

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
        bit_t1 = np.arange(start = 0, stop = self.Tc * q, step = 1/(self.Fs*0.5))
        bit_L = len(bit_t)
        bit_L1 = len(bit_t1)
        tempseq = self.Mseq_GEN(order,index, self.taps)
        print(tempseq); print(len(tempseq))
        s_bb = upfirdn(h = [1]*bit_L, x = 2*tempseq -1 , up = bit_L)
        s_bb1 = upfirdn(h = [1]*bit_L1, x = 2*tempseq -1 , up = bit_L1)
        coef = upfirdn(h = [1]*bit_L, x = tempseq , up = bit_L)
        symbol_t = np.arange(start = 0, stop = len(s_bb))*(1/self.Fs)
        symbol_t1 = np.arange(start = 0, stop = len(s_bb1))*(1/(self.Fs*0.5))
        carrier = np.sin(2*np.pi*self.Rc*symbol_t)
        carrier1 = np.sin(2*np.pi*self.Rc*symbol_t1)

        print(len(carrier))
        print()
        y = []
        for i in range(0, r):
            y.extend(s_bb * carrier)
        y = np.array(y)
        y1 = s_bb1 * carrier1
        with TdmsWriter("F:/4. NI SW/3차원해수유동 국책과제/TRX_CONTROLLER_SIMULATRO_1.2/3. TDMS/Coef88.tdms") as tdms_writer:
            channel = ChannelObject('A', 'Data', y)
            tdms_writer.write_segment([channel])
            channel = ChannelObject('A', 'Mask', tempseq)
            tdms_writer.write_segment([channel])
            channel = ChannelObject('A', 'Mm', y1)
            tdms_writer.write_segment([channel])
        # plt.subplot(1,2,1)
        # plt.plot(symbol_t,s_bb, 'ro--')
        # plt.plot(symbol_t, y,'go-')
        # plt.grid();plt.xlabel('Time(sec)');plt.ylabel('Amplitude(V)');plt.title('Modulation Signal Generate with PN-CODE')
        # plt.tight_layout()
        # NFFT = len(y)
        # Y = fftshift(fft(y, NFFT)*(1/NFFT))
        # f = np.arange(start = -NFFT/2, stop = NFFT/2)*(self.Fs/NFFT)
        # plt.subplot(1,2,2)
        # plt.plot(f,abs(Y))
        # plt.grid();plt.xlabel('Frequency(kHz)');plt.ylabel('Magnitude');plt.title('FFT Result')
        # plt.tight_layout()      
        return  coef, y
    def sig(self,coef,y):
        with TdmsFile.open("F:/4. NI SW/3차원해수유동 국책과제/TRX_CONTROLLER_SIMULATRO_1.0/3. TDMS/Result.tdms") as tdms_file:
            group = tdms_file['B']
            channel = group['Data']
            channel_data = channel[:]


            filtered_y = signal.correlate(y, channel_data, method = 'fft')

            plt.figure()
            plt.plot(filtered_y)

        # filtered_y = signal.correlate(y, y, method = 'fft')
        # plt.figure()
        # plt.plot(filtered_y)
        
    def main(self):
        coef, y = self.SIG_GEN(4,1,8,0)
        # self.sig(coef, y)
if __name__ == "__main__":
    print('START')
    A = Simulator()
    A.main()
    plt.show()