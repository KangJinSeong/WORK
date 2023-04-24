
'''
Date: 2022.12.22
Title: DVL 시뮬레이터 파악 소스코드(TEST)
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

# with open('C:/Users/USER/Desktop/DSP_python/test/soyang_0611sw.txt','r') as file:
#     raw = file.read()

# with open('C:/Users/USER/Desktop/DSP_python/test/soyang_0612sw_1.txt','r') as file:
#     raw = file.read()

with open('C:/Users/USER/Desktop/DSP_python/test/Water_1m_1ms_140609_Moving.txt','r') as file:
    raw = file.read()    


data = raw.split('\n')
data = data[1:-2]
data = [int(i) for i in data]

Fs = 160e3
Fc = 40e3

data = data[:16000]


t = np.arange(start= 0, stop = len(data))*(1/Fs)

NFFT = len(data)
DATA = fftshift(fft(data, NFFT)*(1/NFFT))
f = np.arange(start = -NFFT/2, stop = NFFT/2)*(Fs/NFFT)

plt.subplot(2,1,1)
plt.plot(t,data)
plt.xlabel('Time(sec)');plt.ylabel('ADC RESULT')
plt.title('Water_1m_1ms_140609_Moving Data')
plt.tight_layout()
plt.subplot(2,1,2)
plt.psd(data, NFFT, Fs)
# plt.plot(f,abs(DATA))
# plt.xlabel('Frequency(kHz)');plt.ylabel('Magnitude')
# plt.title('Data FFT Result')
plt.tight_layout()

f, t, Zxx = signal.stft(data, Fs, nperseg=256, noverlap=(256*3)//10)
Z = abs(Zxx)
Z = 20*np.log10(Z)
print(Z[:10])

plt.figure()
plt.pcolormesh(t, f, Z, cmap='inferno')
plt.colorbar()
plt.title('STFT Magnitude')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')

plt.show()





