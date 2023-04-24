'''
Date: 2022.12.28
Title: 어구자동식별모니터링 데이터 시뮬레이터(Phase)
By: Kang Jin Seong
'''

import numpy as np
from pylfsr import LFSR
import matplotlib.pyplot as plt
from scipy.signal import upfirdn
from scipy.fftpack import fft, ifft, fftshift, ifftshift
from scipy import signal
from matplotlib import font_manager, rc
import ICAT_Simulator as ICAT

font_path = "C:/Windows/Fonts/gulim.ttc"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)



class Simulator(ICAT.Analytic):
    def __init__(self):
        super().__init__()
        self.Rc = 32e3
        self.Tc = 1/self.Rc
        self.Fs = self.Rc * 4 # 기존 값 : 4 , 8
        self.Fc = self.Rc
        self.decimaterate = 16
        self.dFs = int(self.Fs / self.decimaterate)
        self.taps = [8,7,6,1]
        self.taps1 = [8,5,3,1]
    def analog(self):
        S_BB, y1 =self.mod_IQ(q = 16,r = 1,order = 8, index = 0, taps= self.taps)
        S_BB1, y2 =self.mod_IQ(q = 16,r = 1,order = 8, index = 4,taps= self.taps1)
        p1 = []
        p1.extend([0]*10)
        p1.extend(y1)
        p1.extend([0]*90)
        p2 = []
        p2.extend([0]*100)
        p2.extend(y2)
        
        # y = np.array(p1) + np.array(p2)   # PN CODE 2개 합 신호
        y = y1



        # PN CODE 2개 합 신호 그리기
        t1 = np.arange(0,len(y)/self.Fs, 1/self.Fs)
        # print(len(t1), len(p1), len(p2))
        # plt.figure()
        # plt.plot(t1,p1);plt.plot(t1,p2);plt.grid()


        Demode_carrier_I = np.sin(2*np.pi*self.Rc*t1)
        Demode_carrier_Q = -np.sin(2*np.pi*self.Rc*t1)
        rx_Q = y * Demode_carrier_Q
        rx_I = y * Demode_carrier_I
        fir = signal.firwin(63, cutoff=10000,fs=self.Fs, pass_zero='lowpass')
        result_r_I = signal.lfilter(fir, [1.0],rx_I)
        print(len(y), len(result_r_I))
        result_r_Q = signal.lfilter(fir, [1.0],rx_Q)
        result = result_r_I.real + 1j*result_r_Q.imag
        NFFT = len(result)
        RESULT = fftshift(fft(result,NFFT)*(1/NFFT))
        RX_I = fftshift(fft(rx_I,NFFT)*(1/NFFT))
        RX_Q = fftshift(fft(rx_Q,NFFT)*(1/NFFT))
        RESULT_R_I = fftshift(fft(result_r_I,NFFT)*(1/NFFT))
        RESULT_R_Q = fftshift(fft(result_r_Q,NFFT)*(1/NFFT))
        Y = fftshift(fft(y,NFFT)*(1/NFFT))
        f = np.arange(start = -NFFT/2, stop = NFFT/2)*(self.Fs/NFFT) 

        fig1, ax = plt.subplots(nrows = 3, ncols = 2)
        ax[0,0].plot(t1,y);ax[0,0].set_xlabel('Time(sec)');ax[0,0].set_ylabel('Amplitude(V)');ax[0,0].grid();ax[0,0].set_title('Receive Signal')
        ax[0,1].plot(f,abs(Y));ax[0,1].set_xlabel('Frequency(Hz)');ax[0,1].set_ylabel('Magnitude');ax[0,1].grid();ax[0,1].set_title('FFT with Receive Singal')
        ax[1,0].plot(t1,rx_I);ax[1,0].set_xlabel('Time(sec)');ax[1,0].set_ylabel('Amplitude(V)');ax[1,0].grid();ax[1,0].set_title('Demodulation Singal')
        ax[1,1].plot(f,abs(RX_I));ax[1,1].set_xlabel('Frequency(Hz)');ax[1,1].set_ylabel('Magnitude');ax[1,1].grid();ax[1,1].set_title('FFT With Demodulation Singal')
        ax[2,0].plot(t1,result_r_I);ax[2,0].set_xlabel('Time(sec)');ax[2,0].set_ylabel('Amplitude(V)');ax[2,0].grid();ax[2,0].set_title('Filtering Signal')
        ax[2,1].plot(f,abs(RESULT_R_I));ax[2,1].set_xlabel('Frequency(Hz)');ax[2,1].set_ylabel('Magnitude');ax[2,1].grid();ax[2,1].set_title('FFT With Filtering Signal')
              
        # fig2, ax = plt.subplots(nrows = 3, ncols = 2)
        # ax[0,0].plot(t1,y);ax[0,0].set_xlabel('Time(sec)');ax[0,0].set_ylabel('Amplitude(V)');ax[0,0].grid();ax[0,0].set_title('Receive Signal')
        # ax[0,1].plot(f,abs(Y));ax[0,1].set_xlabel('Frequency(Hz)');ax[0,1].set_ylabel('Magnitude');ax[0,1].grid();ax[0,1].set_title('FFT with Receive Singal')
        # ax[1,0].plot(t1,rx_Q);ax[1,0].set_xlabel('Time(sec)');ax[1,0].set_ylabel('Amplitude(V)');ax[1,0].grid();ax[1,0].set_title('Demodulation Singal')
        # ax[1,1].plot(f,abs(RX_Q));ax[1,1].set_xlabel('Frequency(Hz)');ax[1,1].set_ylabel('Magnitude');ax[1,1].grid();ax[1,1].set_title('FFT With Demodulation Singal')
        # ax[2,0].plot(t1,result_r_Q);ax[2,0].set_xlabel('Time(sec)');ax[2,0].set_ylabel('Amplitude(V)');ax[2,0].grid();ax[2,0].set_title('Filtering Signal')
        # ax[2,1].plot(f,abs(RESULT_R_Q));ax[2,1].set_xlabel('Frequency(Hz)');ax[2,1].set_ylabel('Magnitude');ax[2,1].grid();ax[2,1].set_title('FFT With Filtering Signal')



        return S_BB,S_BB1, result, t1, f

    def ADC(self):
        S_BB ,S_BB1, result,t,f = self.analog()
        d_result = signal.decimate(result, self.decimaterate)
        d_S_BB = signal.decimate(S_BB, self.decimaterate)
        # d_S_BB1 = signal.decimate(S_BB1, self.decimaterate)
        t1 = np.arange(0, len(d_result)/self.dFs, 1/self.dFs)
        fig2, ax = plt.subplots(nrows = 2, ncols = 2)
        ax[0,0].plot(t,result.real);ax[0,0].set_xlabel('Time(sec)');ax[0,0].set_ylabel('Amplitude(V)');ax[0,0].grid();ax[0,0].set_title('Receive Signal(I(t))')
        ax[0,1].plot(t1,d_result.real);ax[0,1].set_xlabel('Time(sec)');ax[0,1].set_ylabel('Amplitude(V)');ax[0,1].grid();ax[0,1].set_title('Decimate Signal(I(t))')
        ax[1,0].plot(t,result.imag);ax[1,0].set_xlabel('Time(sec)');ax[1,0].set_ylabel('Amplitude(V)');ax[1,0].grid();ax[1,0].set_title('Receive Signal(Q(t))')
        ax[1,1].plot(t1,d_result.imag);ax[1,1].set_xlabel('Time(sec)');ax[1,1].set_ylabel('Amplitude(V)');ax[1,1].grid();ax[1,1].set_title('Decimate Signal(Q(t))')

        filtered_y = signal.correlate(d_S_BB.real, d_result.real, method = 'fft')
        # filtered_y1 = signal.correlate(d_S_BB1.real, d_result.real, method = 'fft')
        en_filtered_y = abs(signal.hilbert(np.diff(filtered_y)))
        # en_filtered_y1 = abs(signal.hilbert(np.diff(filtered_y1))) 
        t2 = np.arange(0, len(en_filtered_y )/self.dFs, 1/self.dFs)
        plt.figure()
        plt.plot(t2,en_filtered_y, label = 'Taps1')
        # plt.plot(t2,en_filtered_y1, label = 'Taps2')
        plt.grid()
        plt.title('Cross-Correlation Result');plt.xlabel('Time(sec)');plt.ylabel('Correlation');plt.legend()

    def main(self):
        self.ADC()
    #    self.Demod(coef= coef, y = y,window_size=1, cut_f= 32e3)

if __name__ == "__main__":
    print('SSS')
    A = Simulator()
    A.main()
    plt.show()