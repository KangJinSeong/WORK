'''
Date: 2023.03.17
Title: 어구자동식별모니터링 데이터 시뮬레이터(PPM)
By: Kang Jin Seong
'''

import numpy as np
from pylfsr import LFSR
import matplotlib.pyplot as plt
from scipy.signal import upfirdn
from scipy.fftpack import fft, ifft, fftshift, ifftshift
from scipy import signal
from matplotlib import font_manager, rc
import EFG_Simulator as EFG

font_path = "C:/Windows/Fonts/gulim.ttc"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

class Simulator(EFG.Simulator):
    def __init__(self):
        super().__init__()

    def main(self):
        coef, y, s_bb = self.SIG_GEN(q = 16, r = 1, order = 8, index= 0)
        
        NFFT = len(s_bb)
        RESULT = fftshift(fft(s_bb,NFFT)*(1/NFFT))
        f = np.arange(start = -NFFT/2, stop = NFFT/2)*(self.Fs/NFFT)        
        
    
        fig1, ax = plt.subplots(nrows = 1, ncols = 2)
        ax[0].plot(s_bb);ax[0].set_xlabel('Number(N)');ax[0].set_ylabel('Amplitude(V)');ax[0].grid();ax[0].set_title('Receive Singal with PN-CODE')
        ax[1].plot(f,abs(RESULT));ax[1].set_xlabel('Frequency(Hz)');ax[1].set_ylabel('Magnitude');ax[1].grid();ax[1].set_title('FFT with Receive Singal')

        filtered_y = signal.correlate(s_bb, s_bb, method = 'fft')
        en_filtered_y = abs(signal.hilbert(np.diff(filtered_y)))

        plt.figure()
        plt.plot(en_filtered_y)
        plt.grid()
        plt.title('Cross-Correlation Result');plt.xlabel('Time(sec)');plt.ylabel('Correlation')


if __name__ == "__main__":
    print('PPM')
    A = Simulator()
    A.main()
    plt.show()