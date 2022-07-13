#%%

'''
Date: 2021.09.02
Title: Dry Unit v2.1
By: Kang Jin Seong
'''
import time
import pandas as pd
from scipy.fftpack import fft, ifft, fftshift, ifftshift
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import chirp, hilbert
from scipy import signal
from scipy.signal import upfirdn
from queue import Queue

a = time.time()

'''
ADC device Setup
'''
fs = 32000*8*8 # sampling frequency

'''
Chirpping signal generate
'''
t = np.arange(start = 0, stop = 0.128, step = 1/fs) #Chirp time base
g1 = chirp(t, f0= 30000, t1 = 0.128, f1 = 34000, method = 'linear') # UP-chirpping signal(coefficient for bit 1)
g2 = chirp(t, f0= 34000, t1 = 0.128, f1 = 30000, method = 'linear') # DOWN-chirpping signal(coefficient for bit 0)

'''
receive signal generate
'''
#다른 길이의 벡터를 붙히기 위한 array 배열의 list 배열로 변환
zero_s = (np.zeros((1,int(0.1*fs))).tolist())[0]
zero_e = (np.zeros((1,int(0.2*fs))).tolist())[0]
zero1_s = (np.zeros((1,int(0.15*fs))).tolist())[0]

r_ch1 = []
r_ch1.extend(zero_s)
r_ch1.extend(g1) #bit 1
r_ch1.extend(g2) #bit 0
r_ch1.extend(g1) #bit 1
r_ch1.extend(g1) #bit 1
r_ch1.extend(g2) #bit 0
r_ch1.extend(zero_e)

r_ch2 = []
r_ch2.extend(zero1_s)
r_ch2.extend(g1)
r_ch2.extend(g2)
r_ch2.extend(g1)
r_ch2.extend(g1)
r_ch2.extend(g2)
r_ch2.extend(zero1_s)

#계산을 위한 list 배열의 array 배열 변환
r_ch1 = np.array(r_ch1)
r_ch2 = np.array(r_ch2)

r_t = np.arange(start=0,stop=len(r_ch1))*1/fs

'''
signal processing using FFT convolve
'''

y1_ch1 = signal.correlate(r_ch1,g1, method= 'fft')     # using FFT cross-correlation
y2_ch1 = signal.correlate(r_ch1,g2, method= 'fft')     # using FFT cross-correlation

y1_ch2 = signal.correlate(r_ch2,g1, method= 'fft')     # using FFT cross-correlation
y2_ch2 = signal.correlate(r_ch2,g2, method= 'fft')     # using FFT cross-correlation

en1_ch1 = abs(hilbert(np.diff(y1_ch1)))  # envelop detect of cross correlate result - bit 1
en2_ch1 = abs(hilbert(np.diff(y2_ch1)))  # envelop detect of cross correlate result - bit 0

en1_ch2 = abs(hilbert(np.diff(y1_ch2)))  # envelop detect of cross correlate result - bit 1
en2_ch2 = abs(hilbert(np.diff(y2_ch2)))  # envelop detect of cross correlate result - bit 0

en1_y = en1_ch1 - en2_ch1 # 두 신호차를 이용한 White noise 제거
en2_y = en1_ch2 - en2_ch2 # 두 신호차를 이용한 White noise 제거

en1_y = en1_y/max(en1_y)
en2_y = en2_y/max(en2_y)

y_t = np.arange(start = 0, stop = len(y1_ch1))*1/fs # cross-correlation(FFT)결과 값의 Time base
en_t = np.arange(start = 0, stop = len(en1_y))*1/fs  # Envelope 결과 값의 Time base

'''
signal processing using moving average
'''

y_ch1 = pd.Series(en1_y)
ma_y_ch1 = y_ch1.rolling(160).mean()
ma_y_ch1 = np.array(ma_y_ch1)
ma_y_ch1 = ma_y_ch1[159:]

'''
signal Threshold 
'''

yt_p = max(ma_y_ch1) * 0.7  #최대 값의 70%를 임계값으로 설정
yt_n = min(ma_y_ch1) * 0.7

Peaks_ind0, _ = signal.find_peaks(en1_y, height= yt_p, distance= len(g1))    # 임계값 이상, 거리가 coefficient 길이가 맞는 신호의 대한 인덱스 값 추출
Peaks_ind1, _ = signal.find_peaks(-en1_y, height= -yt_n, distance= len(g1)) 

#다른 길이의 벡터를 붙히기 위한 array 배열의 list 배열로 변환
Peaks_ind0 =  Peaks_ind0.tolist()
Peaks_ind1 =  Peaks_ind1.tolist()

index = []  # 코드 확인을 위한 인덱스 값 배열 합치기 및 오름차순 정렬
index.extend(Peaks_ind0)
index.extend(Peaks_ind1)
index.sort()

# 수신 ID 코드
code = ((np.ones((1,5))*-1).tolist())[0]

# 추출한 인덱스로 부터 각 배열마다 Coeff 1, Coeff 0의 인덱스 인지 확인
# Coeff 0 의 값과 동일 하다면 RX bit = 1
# Coeff 1 의 값과 동일 하다면 RX bit = 0
for i in range(0, len(index)):
    for j in range(0, len(Peaks_ind0)):
        if index[i] == Peaks_ind0[j]:
            code.pop(0)
            code.append(1)
    for k in range(0, len(Peaks_ind1)):
        if index[i] == Peaks_ind1[k]:
            code.pop(0)
            code.append(0)

b = time.time()
print('time : ', b-a)
'''
Noise Channel
'''
snr_dB = 6            #SNR in dB
snr = pow(10,snr_dB/10)    #linear SNR
signal_power = pow(np.linalg.norm(r_ch1),2)/len(r_t)    #modulated signal power(신호벡터크기 계산)

noise_power = signal_power/snr  #noise power

noise_std = np.sqrt(noise_power)    #noise standard deviation

noise = noise_std*np.random.normal(size = (len(r_t))) # awgn noise

n_r_ch1 = noise + r_ch1
n_r_ch2 = noise + r_ch2

n_y1_ch1 = signal.correlate(n_r_ch1,g1, method= 'fft')     # using FFT cross-correlation
n_y2_ch1 = signal.correlate(n_r_ch1,g2, method= 'fft')     # using FFT cross-correlation

n_y1_ch2 = signal.correlate(n_r_ch2,g1, method= 'fft')     # using FFT cross-correlation
n_y2_ch2 = signal.correlate(n_r_ch2,g2, method= 'fft')     # using FFT cross-correlation

n_en1_ch1 = abs(hilbert(np.diff(n_y1_ch1)))  # envelop detect of cross correlate result - bit 1
n_en2_ch1 = abs(hilbert(np.diff(n_y2_ch1)))  # envelop detect of cross correlate result - bit 0

n_en1_ch2 = abs(hilbert(np.diff(n_y1_ch2)))  # envelop detect of cross correlate result - bit 1
n_en2_ch2 = abs(hilbert(np.diff(n_y2_ch2)))  # envelop detect of cross correlate result - bit 0

n_en1_y = n_en1_ch1 - n_en2_ch1 # 두 신호차를 이용한 White noise 제거
n_en2_y = n_en1_ch2 - n_en2_ch2 # 두 신호차를 이용한 White noise 제거

n_en1_y = n_en1_y/max(n_en1_y)
n_en2_y = n_en2_y/max(n_en2_y)

print('code = ', code)

fig1, (axs1,axs2) = plt.subplots(nrows = 2, ncols = 1)
axs1.plot(r_t, r_ch1,'b', label = 'Sensor#1')
axs1.plot(r_t, r_ch2,'r', label = 'Sensor#2');axs1.set_xlabel('Time(s)');axs1.set_ylabel('Amplitude')
axs1.legend(loc = 'upper right')
# axs[0,0].set_ylim(-2,2)
axs2.plot(en_t, en1_y,'b',label = 'Sensor#1')
axs2.plot(en_t, en2_y,'r', label = 'Sensor#2')
axs2.legend(loc = 'upper right')
fig1.tight_layout()
fig1.show()

fig2, (axs3,axs4) = plt.subplots(nrows = 2, ncols = 1)
axs3.plot(r_t, n_r_ch1,'b', label = 'Sensor#1')
axs3.plot(r_t, n_r_ch2,'r', label = 'Sensor#2');axs1.set_xlabel('Time(s)');axs1.set_ylabel('Amplitude')
axs3.legend(loc = 'upper right')
# axs[0,0].set_ylim(-2,2)
axs4.plot(en_t, n_en1_y,'b',label = 'Sensor#1')
axs4.plot(en_t, n_en2_y,'r', label = 'Sensor#2')
axs4.legend(loc = 'upper right')
fig2.tight_layout()
fig2.show()

plt.show()

# fig1.savefig(r'C:\Users\USER\Desktop\DSP_python\FSK signal modulation.png', dpi = 100)

# %%
