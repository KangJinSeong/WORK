
'''
Date: 2022.12.15
Title: 히로시마 장비 데이터 시뮬레이터
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
        self.Fs = 40e3
        self.Rc = 10e3
        self.Tc = 1/self.Rc
        self.Fc = self.Rc * 4

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
        print(tempseq)
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
        return  coef, y, s_bb

    def Demod(self, coef,y, window_size, cut_f):
        t1 = np.arange(0,len(y)/self.Fs, 1/self.Fs)
        Demode_carrier = np.sin(2*np.pi*self.Rc*t1)
        rx = y * Demode_carrier
        fir = signal.firwin(512, cutoff=cut_f,fs=self.Fs, pass_zero='lowpass')
        result_r = signal.lfilter(fir, [1.0],rx)

        NFFT = len(result_r)
        RX = fftshift(fft(rx,NFFT)*(1/NFFT))
        Y = fftshift(fft(y,NFFT)*(1/NFFT))
        RESULT_R = fftshift(fft(result_r,NFFT)*(1/NFFT))
        f = np.arange(start = -NFFT/2, stop = NFFT/2)*(self.Fs/NFFT)

        moving_averages = []
        i = 0
        while i < len(result_r) - window_size + 1:
            window_average = round(np.sum(result_r[i:i+window_size])/ window_size, 2)
            moving_averages.append(window_average)
            i += 1

        fig1, ax = plt.subplots(nrows = 3, ncols = 2)
        ax[0,0].plot(t1,y);ax[0,0].set_xlabel('Time(sec)');ax[0,0].set_ylabel('Amplitude(V)');ax[0,0].grid();ax[0,0].set_title('Receive Signal')
        ax[0,1].plot(f,abs(Y));ax[0,1].set_xlabel('Frequency(Hz)');ax[0,1].set_ylabel('Magnitude');ax[0,1].grid();ax[0,1].set_title('FFT with Receive Singal')
        ax[1,0].plot(t1,rx);ax[1,0].set_xlabel('Time(sec)');ax[1,0].set_ylabel('Amplitude(V)');ax[1,0].grid();ax[1,0].set_title('Demodulation Singal')
        ax[1,1].plot(f,abs(RX));ax[1,1].set_xlabel('Frequency(Hz)');ax[1,1].set_ylabel('Magnitude');ax[1,1].grid();ax[1,1].set_title('FFT With Demodulation Singal')
        ax[2,0].plot(t1,result_r);ax[2,0].set_xlabel('Time(sec)');ax[2,0].set_ylabel('Amplitude(V)');ax[2,0].grid();ax[2,0].set_title('Filtering Signal')
        ax[2,1].plot(f,abs(RESULT_R));ax[2,1].set_xlabel('Frequency(Hz)');ax[2,1].set_ylabel('Magnitude');ax[2,1].grid();ax[2,1].set_title('FFT With Filtering Signal')
        
        
        # plt.tight_layout()

        moving_averages = (moving_averages - min(moving_averages)) / (max(moving_averages) - min(moving_averages))
        filtered_y = signal.correlate(coef, moving_averages, method = 'fft')
        en_filtered_y = abs(signal.hilbert(np.diff(filtered_y)))
        fig2, (ax1,ax2,ax3) = plt.subplots(nrows = 3, ncols = 1)
        ax1.plot(moving_averages);ax1.set_xlabel('Number of sampling(N)');ax1.set_ylabel('Amplitude(V)');ax1.set_title('Movigne Average(N=5) & Normalization');ax1.grid()
        ax2.plot(coef);ax2.set_xlabel('Number of sampling(N)');ax2.set_ylabel('Amplitude(V)');ax2.set_title('Coeficent Result');ax2.grid()
        ax3.plot(en_filtered_y);ax3.set_xlabel('Number of sampling(N)');ax3.set_ylabel('Magnitude');ax3.set_title('Matched Filter Result');ax3.grid()
        # plt.tight_layout()

    def mod_IQ(self,q,r,order, index, taps):
        bit_t = np.arange(start = 0, stop = self.Tc * q, step = 1/self.Fs)
        bit_L = len(bit_t)
        tempseq = self.Mseq_GEN(order,index,taps)
        print(tempseq)
        s_bb = upfirdn(h = [1]*bit_L, x = 2*tempseq -1 , up = bit_L)
        symbol_t = np.arange(start = 0, stop = len(s_bb))*(1/self.Fs)
        S_BB = ifft(fft(s_bb, len(s_bb)))
        SIG = S_BB.real*np.cos(2*np.pi*self.Fc*symbol_t) + 1j*S_BB.imag*np.sin(2*np.pi*self.Fc*symbol_t)

        print(SIG[:10])
        y = []
        for i in range(0, r):
            # y.extend(SIG)
            y.extend(s_bb *np.sin(2*np.pi*self.Fc*symbol_t))    # 시뮬레이션을 위한 실험 값
        y = np.array(y)
        # plt.figure()
        # plt.plot(symbol_t,s_bb, 'ro--')
        # plt.plot(symbol_t, y,'go-')
        # plt.grid();plt.xlabel('Time(sec)');plt.ylabel('Amplitude(V)');plt.title('Modulation Signal Generate with PN-CODE')
        # plt.tight_layout()
        return  S_BB, y

    def Demod_IQ(self, coef,y):
        t1 = np.arange(0,len(y)/self.Fs, 1/self.Fs)
        Demode_carrier_I = np.cos(2*np.pi*self.Rc*t1)
        Demode_carrier_Q = -np.sin(2*np.pi*self.Rc*t1)
        rx_Q = y * Demode_carrier_Q
        rx_I = y * Demode_carrier_I
        fir = signal.firwin(512, cutoff=5000,fs=self.Fs, pass_zero='lowpass')
        result_r_I = signal.lfilter(fir, [1.0],rx_I)
        result_r_Q = signal.lfilter(fir, [1.0],rx_Q)

        NFFT = len(result_r_I)
        Y = fftshift(fft(y,NFFT)*(1/NFFT))
        RX_Q = fftshift(fft(rx_Q,NFFT)*(1/NFFT))
        RX_I = fftshift(fft(rx_I,NFFT)*(1/NFFT))
        RESULT_R_I = fftshift(fft(result_r_I,NFFT)*(1/NFFT))
        RESULT_R_Q = fftshift(fft(result_r_Q,NFFT)*(1/NFFT))
        f = np.arange(start = -NFFT/2, stop = NFFT/2)*(self.Fs/NFFT)

        fig1, ax = plt.subplots(nrows = 3, ncols = 2)
        ax[0,0].plot(t1,y);ax[0,0].set_xlabel('Time(sec)');ax[0,0].set_ylabel('Amplitude(V)');ax[0,0].grid();ax[0,0].set_title('Receive Signal')
        ax[0,1].plot(f,abs(Y));ax[0,1].set_xlabel('Frequency(Hz)');ax[0,1].set_ylabel('Magnitude');ax[0,1].grid();ax[0,1].set_title('FFT with Receive Singal')
        ax[1,0].plot(t1,rx_I);ax[1,0].set_xlabel('Time(sec)');ax[1,0].set_ylabel('Amplitude(V)');ax[1,0].grid();ax[1,0].set_title('Demodulation Singal')
        ax[1,1].plot(f,abs(RX_I));ax[1,1].set_xlabel('Frequency(Hz)');ax[1,1].set_ylabel('Magnitude');ax[1,1].grid();ax[1,1].set_title('FFT With Demodulation Singal')
        ax[2,0].plot(t1,result_r_I);ax[2,0].set_xlabel('Time(sec)');ax[2,0].set_ylabel('Amplitude(V)');ax[2,0].grid();ax[2,0].set_title('Filtering Signal')
        ax[2,1].plot(f,abs(RESULT_R_I));ax[2,1].set_xlabel('Frequency(Hz)');ax[2,1].set_ylabel('Magnitude');ax[2,1].grid();ax[2,1].set_title('FFT With Filtering Signal')
              
        fig2, ax = plt.subplots(nrows = 3, ncols = 2)
        ax[0,0].plot(t1,y);ax[0,0].set_xlabel('Time(sec)');ax[0,0].set_ylabel('Amplitude(V)');ax[0,0].grid();ax[0,0].set_title('Receive Signal')
        ax[0,1].plot(f,abs(Y));ax[0,1].set_xlabel('Frequency(Hz)');ax[0,1].set_ylabel('Magnitude');ax[0,1].grid();ax[0,1].set_title('FFT with Receive Singal')
        ax[1,0].plot(t1,rx_Q);ax[1,0].set_xlabel('Time(sec)');ax[1,0].set_ylabel('Amplitude(V)');ax[1,0].grid();ax[1,0].set_title('Demodulation Singal')
        ax[1,1].plot(f,abs(RX_Q));ax[1,1].set_xlabel('Frequency(Hz)');ax[1,1].set_ylabel('Magnitude');ax[1,1].grid();ax[1,1].set_title('FFT With Demodulation Singal')
        ax[2,0].plot(t1,result_r_Q);ax[2,0].set_xlabel('Time(sec)');ax[2,0].set_ylabel('Amplitude(V)');ax[2,0].grid();ax[2,0].set_title('Filtering Signal')
        ax[2,1].plot(f,abs(RESULT_R_Q));ax[2,1].set_xlabel('Frequency(Hz)');ax[2,1].set_ylabel('Magnitude');ax[2,1].grid();ax[2,1].set_title('FFT With Filtering Signal')

        filtered_y = signal.correlate(coef.real, result_r_I.real, method = 'fft')
        filtered_y1 = signal.correlate(coef.imag, result_r_Q.imag, method = 'fft')
        en_filtered_y = abs(signal.hilbert(np.diff(filtered_y)))
        en_filtered_y1 = abs(signal.hilbert(np.diff(filtered_y1)))

        fig3, (ax1,ax2) = plt.subplots(nrows = 2, ncols = 1)
        ax1.plot(coef.real);ax1.set_xlabel('Number of sampling(N)');ax1.set_ylabel('Amplitude(V)');ax1.set_title('Movigne Average(N=5) & Normalization');ax1.grid()
        ax2.plot(en_filtered_y);ax2.set_xlabel('Number of sampling(N)');ax2.set_ylabel('Amplitude(V)');ax2.set_title('Coeficent Result');ax2.grid()
        fig4, (ax1,ax2) = plt.subplots(nrows = 2, ncols = 1)
        ax1.plot(coef.imag);ax1.set_xlabel('Number of sampling(N)');ax1.set_ylabel('Amplitude(V)');ax1.set_title('Movigne Average(N=5) & Normalization');ax1.grid()
        ax2.plot(en_filtered_y1);ax2.set_xlabel('Number of sampling(N)');ax2.set_ylabel('Amplitude(V)');ax2.set_title('Coeficent Result');ax2.grid()
        return result_r_I, result_r_Q
        # plt.tight_layout()


    def main(self):
        s_bb, y = self.mod_IQ(3,1,8,0)
        self.Demod_IQ(s_bb,y)
class Analytic(Simulator):
    def __init__(self):
        super().__init__()
    
    def simulation_sig_gen(self,delta_time):
        coef, y = self.SIG_GEN(3,1,8,0)
        coef1,y1 = self.SIG_GEN(3,1,8,0)
        delta_L = int(delta_time * self.Fs)
        print(len(y), delta_L)

        A_y = []
        A_y.extend(y)
        A_y.extend(np.zeros(delta_L, int))   #delta_L
        A_y.extend(np.zeros(3072, int)) #len(y1)
        A_y = np.array(A_y)

        B_y = []
        B_y.extend(np.zeros(delta_L, int))
        B_y.extend(y1) #len(y1)
        B_y.extend(np.zeros(3072, int)) #len(y)
        B_y = np.array(B_y)

        TX_SIG = A_y + B_y

        t = np.arange(start = 0, stop = len(A_y))*(1/self.Fs)

        plt.figure()
        plt.plot(t,A_y)
        plt.plot(t,B_y, 'g')
        plt.tight_layout()
        return coef, TX_SIG, y
    
    def KW_Demod(self, coef, y):
        y = (y - min(y)) / (max(y) - min(y))
        filtered_y =  signal.correlate(coef,y, method='fft')
        en_filtered_y = abs(signal.hilbert(np.diff(filtered_y)))
        fig1, (ax1,ax2,ax3) = plt.subplots(nrows = 3, ncols = 1)
        ax1.plot(y);ax1.set_xlabel('Number of sampling(N)');ax1.set_ylabel('Amplitude(V)');ax1.set_title('Receive Signal');ax1.grid()
        ax2.plot(coef);ax2.set_xlabel('Number of sampling(N)');ax2.set_ylabel('Amplitude(V)');ax2.set_title('Coeficent Result');ax2.grid()
        ax3.plot(en_filtered_y);ax3.set_xlabel('Number of sampling(N)');ax3.set_ylabel('Magnitude');ax3.set_title('Matched Filter Result');ax3.grid()
        plt.tight_layout()


    def main(self):
        coef, TX_SIG, y = self.simulation_sig_gen(self.Tc * 2)
        self.Demod(coef,TX_SIG,5)
        self.KW_Demod(coef, TX_SIG)
if __name__ == "__main__":
    print('START')
    A = Simulator()
    A.main()
    B = Analytic()
    # B.main()
    plt.show()

