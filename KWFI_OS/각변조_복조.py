'''
Date: 2021.11.16
Title: 
By: Kang Jin Seong
'''

from scipy.fftpack import fft, ifft, fftshift, ifftshift
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert


class Mod_DeMod:
    def __init__(self):
        self.T = 1/2000
        self.Fs = 1/self.T
        self.fc = 300
        self.t = np.arange(0,0.15,self.T)
        self.kf = 50
    
    def generate_signal(self):
        y = np.zeros(int(0.15/self.T))
        y[0:100] = 1
        y[100:200] = -2
        y[200:300] = 0
        return y
        # plt.plot(self.t, y)
    def FM_MOD(self, y):
        integ_m = [0] * len(y)
        for i in range(0,len(y)-1):
            integ_m[i+1] = integ_m[i] + y[i]*self.T
        integ_m = np.array(integ_m)
        s_m = np.cos(2*np.pi*((self.fc*self.t)+ (self.kf * integ_m)))
        NFFT = len(s_m)
        Y = fftshift(fft(y,NFFT))
        S_M = fftshift(fft(s_m,NFFT))
        f = np.arange(start = -NFFT/2, stop = NFFT/2)*(self.Fs/NFFT)
        fig1, (ax1, ax2,ax3,ax4) = plt.subplots(nrows = 4, ncols = 1)
        ax1.plot(self.t, y)
        ax2.plot(self.t, s_m)
        ax3.plot(f, abs(Y)/self.Fs)
        ax4.plot(f, abs(S_M)/self.Fs)
        plt.tight_layout()

        return s_m

    def FM_DEMODE(self,y):
        z = hilbert(y)  # 복소수 영역으로 만들기 위해 힐버트 변환 수행
        '''
        동기식 복조 신호
            1) 동기 검파 과정에서는 먼저 수신된 신호로부터 위상을 추출하여 메시지 신호를 적분한 것에 비례하는 신호를 얻는다.
            2) 추출한 위상을 미분한 후 2pikf로 나누어 메시지 신호를 재생한다.
        '''
        i_p = np.unwrap(np.angle(z))
        demod = (1/(2*np.pi*self.kf)*(np.diff(i_p)/self.T))
        '''
        비동기식 복조 신호
         1) 주파수 변별기 사용(수신 신호를 미분하여 진폭이 수신 신호의 순시 주파수에 비례하는 신호를 얻는 다음, 포락선 검파를 사용)
        '''
        z1 = hilbert(np.diff(y))
        inst_amplitude = abs(z1)

        fig1, (ax1, ax2) = plt.subplots(nrows = 2, ncols = 1)
        ax1.plot(self.t[:-1], demod)
        ax2.plot(self.t[:-1], inst_amplitude)
        plt.tight_layout()    

    def main(self):
        y = self.FM_MOD(self.generate_signal())
        self.FM_DEMODE(y)
if __name__ == "__main__":
    print("START")
    A = Mod_DeMod()
    A.main() 
    plt.show()
