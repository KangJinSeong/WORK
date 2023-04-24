'''
Date: 2022.12.02
Title: 
By: Kang Jin Seong
'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import upfirdn, lfilter, hilbert
from matplotlib import font_manager, rc
from scipy.special import erfc
# font_path = "C:\Windows\Fonts\malgun.ttf"
# font = font_manager.FontProperties(fname=font_path).get_name()
# rc('font', family=font)

class MOD:
    def __init__(self):
        self.N = 100000
        self.L = 1000
        self.Fs = 20*self.L
        self.Ts = 1/self.Fs
        self.fc = 5e3
        self.fc2 = 2e3
        # self.b = [1,0,0,1,0,1]
        self.b = np.random.randint(2, size = self.N)
    def OOK(self):
        b = np.array(self.b)
        L = int(1e-3*self.Fs)
        ask_s_bb = upfirdn(h = [1]*L, x = b, up = L)
        t = np.arange(start = 0, stop = len(b)*1e-3, step=self.Ts)
        y = np.cos(2*np.pi*self.fc*t) * ask_s_bb
    
        # print(len(t), len(ask_s_bb))
        # fig1, (ax1, ax2,ax3,ax4) = plt.subplots(nrows = 4, ncols = 1)
        # ax1.plot(t,ask_s_bb);ax1.grid()
        # ax2.plot(t, y);ax2.grid()
        # ax3.psd(ask_s_bb, len(ask_s_bb), self.Fs)
        # ax4.psd(y,len(y), self.Fs)
        # plt.tight_layout()
        return y, t, L

    def FSK(self):
        b = np.array(self.b)
        L = int(1e-3*self.Fs)
        fsk1_s_bb = upfirdn(h = [1]*L, x = b, up = L)
        fsk2_s_bb = upfirdn(h = [1]*L, x = -b+1, up = L)
        fsk_s_bb = fsk1_s_bb - fsk2_s_bb
        t = np.arange(start = 0, stop = 6e-3, step=self.Ts)
        y1 = np.sin(2*np.pi*self.fc*t) * fsk1_s_bb
        y2 = np.sin(2*np.pi*self.fc2*t) * fsk2_s_bb
        coef_y1 = np.sin(2*np.pi*self.fc*t[0:L])
        coef_y2 = np.sin(2*np.pi*self.fc2*t[0:L])
        y = y1 + y2
        fig1, (ax1, ax2,ax3,ax4) = plt.subplots(nrows = 4, ncols = 1)
        ax1.plot(t,fsk_s_bb);ax1.grid()
        ax2.plot(t, y);ax2.grid()
        ax3.psd(fsk_s_bb, len(fsk_s_bb), self.Fs)
        ax4.psd(y,len(y), self.Fs)
        plt.tight_layout()
        return coef_y1, coef_y2, y, t

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

class DEMOD(MOD):
    def __init__(self):
        super().__init__()

    def demod_ASK(self,y,t,L):
        # y,t,L = self.OOK()
        # ASK Demodulation with macthed filter
        coef = np.cos(2*np.pi*self.fc*t[0:L])
        filtered_x = lfilter(coef, 1, y)
        envelope_x = abs(hilbert(filtered_x))
        # Carrier Phase error가 있는 경우 복조기 출력
        coef_phase_error = np.cos(2*np.pi*self.fc*t[0:L] + (30*np.pi/180))
        filtered_x_phase_error = lfilter(coef_phase_error, 1, y)
        envelope_x_phase_error = abs(hilbert(filtered_x_phase_error))
        # Carrier Freuquency error가 있는 경우 복조기 출력
        coef_frequency_error = np.cos(2*np.pi*(self.fc+500)*t[0:L])
        filtered_x_frequency_error = lfilter(coef_frequency_error, 1, y)
        envelope_x_frequency_error = abs(hilbert(filtered_x_frequency_error))       
        # Noncoherent Demodulation
        envelope_y = abs(hilbert(y))
        # fig1, (ax1, ax2,ax3,ax4) = plt.subplots(nrows = 4, ncols = 1)
        # ax1.plot(t,envelope_x);ax1.grid();ax1.set_title('정합필터 출력')
        # ax2.plot(t, envelope_x_phase_error);ax2.grid();ax2.set_title('위상오차가 있는 경우 정합필터 출력')
        # ax3.plot(t, envelope_x_frequency_error);ax3.grid();ax3.set_title('주파수오차가 있는 경우 정합필터 출력')
        # ax4.plot(t, envelope_y);ax4.grid();ax4.set_title('포락선 검출기 출력')
        return envelope_x

    def demod_FSK(self):
        coef_y1, coef_y2, y, t = self.FSK()
        # Coherent FSK Demodulation
        filtered_y1 = lfilter(coef_y1, 1, y)
        filtered_y2 = lfilter(coef_y2, 1, y)
        filtered_x = abs(hilbert(filtered_y1)) - abs(hilbert(filtered_y2))
        # Noncoherent Demodulation
        envelope_y = abs(hilbert(np.diff(y)))
        fig1, (ax1, ax2) = plt.subplots(nrows = 2, ncols = 1)
        ax1.plot(t,filtered_x);ax1.grid();ax1.set_title('FSK 수신기 정합필터 출력')
        ax2.plot(t[:-1], envelope_y);ax2.grid();ax2.set_title('포락선 검출기 출력')
        plt.tight_layout()

    def AWGN(self,snr,y):
        snr_dB = snr           #SNR in dB
        snr = pow(10,snr_dB/10)    #linear SNR
        signal_power = pow(np.linalg.norm(y),2)/len(y)    #modulated signal power(신호벡터크기 계산)
        noise_power = signal_power/snr  #noise power
        noise_std = np.sqrt(noise_power)    #noise standard deviation
        noise = noise_std*np.random.normal(size = (len(y))) # awgn noise
        rx_signal = y+noise
        return rx_signal

    def BER(self):
        EbN0dB = np.arange(start = -4, stop = 11, step= 1)
        SER = np.zeros(len(EbN0dB))
        for i, EbN0 in enumerate(EbN0dB):
            y,t,L = self.OOK()
            rx_signal = self.AWGN(EbN0,y)
            e_y = self.demod_ASK(rx_signal,t,L)
            e_y = e_y[L-1:len(e_y):L]
            b_hat = (e_y > 2).transpose()
            ask_hat = [int(i) for i in b_hat]
            SER[i] = np.sum(self.b != ask_hat)/self.N

        EbN0lins = 10 **(EbN0dB/10)
        theorySER_ASK = 0.5*erfc(np.sqrt(EbN0lins))

        plt.figure()
        plt.semilogy(EbN0dB, SER, 'k*-')
        plt.semilogy(EbN0dB, theorySER_ASK)
        plt.show()



    def main(self):
        # self.demod_ASK()
        # self.demod_FSK()
        self.BER()


if __name__ == "__main__":
    print("START")
    A = DEMOD()
    A.main()
    # plt.show()
