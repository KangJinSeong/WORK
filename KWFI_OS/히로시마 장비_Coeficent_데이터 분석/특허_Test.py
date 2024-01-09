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
        self.Fs = 100e3
        self.Rc = 5e3
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
    
if __name__ == "__main__":
    L = Simulator()
    
    coef,y,s_bb = L.SIG_GEN(2,1,8,0)
    first = []
    second = []
    thrd = []
    for i in y:
        if i == 1:
            first.append(1)
        elif i == -1:
            first.append(-1)
        else:
            first.append(0)
    for i in y:
        if i >= 0.6:
            second.append(1)
        elif i <= -0.6:
            second.append(-1)
        else:
            second.append(0)
    for i in y:
        if i >= 0.2:
            thrd.append(1)
        elif i <= -0.2:
            thrd.append(-1)
        else:
            thrd.append(0)                   

    

    filtered_y = signal.correlate(y, y, method = 'fft')
    filtered_y_frist = signal.correlate(s_bb, first, method = 'fft')
    filtered_y_second = signal.correlate(s_bb, second, method = 'fft')
    filtered_y_thrd = signal.correlate(s_bb, thrd, method = 'fft')
    
    plt.figure()
    plt.subplot(4,1,1)
    plt.plot(filtered_y);plt.title('ADC 후 신호처리한 결과');plt.xlabel('Number of Sample(N)');plt.ylabel('Magnitude');plt.grid()
    plt.subplot(4,1,2)
    plt.plot(filtered_y_frist);plt.title('Comparator 후 신호처리한 결과');plt.xlabel('Number of Sample(N)');plt.ylabel('Magnitude');plt.grid()
    plt.subplot(4,1,3)
    plt.plot(filtered_y_second);plt.title('Comparator(상위 40%) 후 신호처리한 결과');plt.xlabel('Number of Sample(N)');plt.ylabel('Magnitude');plt.grid()
    plt.subplot(4,1,4)
    plt.plot(filtered_y_thrd);plt.title('Comparator(상위 80%) 후 신호처리한 결과');plt.xlabel('Number of Sample(N)');plt.ylabel('Magnitude');plt.grid()



    plt.figure()
    plt.subplot(3,1,1)
    plt.stem(first);plt.title('Comparator 결과');plt.xlabel('Number of Sample(N)');plt.ylabel('Magnitude');plt.grid()
    plt.subplot(3,1,2)
    plt.stem(second);plt.title('Comparator(상위 40%) 결과');plt.xlabel('Number of Sample(N)');plt.ylabel('Magnitude');plt.grid()
    plt.subplot(3,1,3)
    plt.stem(thrd);plt.title('Comparator(상위 80%) 결과');plt.xlabel('Number of Sample(N)');plt.ylabel('Magnitude');plt.grid()

    
    plt.show()
