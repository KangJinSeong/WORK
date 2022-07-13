'''
Date: 2022.02.10
Title: Sonar LOFAR Algorithum test
By: Kang Jin Seong
'''

from cmath import log10
from scipy.fftpack import fft, ifft, fftshift, ifftshift
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

'''
RX_signal Generating (SNR 10dB)
'''
Fs = 192e3  #Sampling Frequency
t = np.arange(start = 0, stop = 10, step = 1/Fs)    #Reciving Singnal time vector
Rx_signal = np.cos(2*np.pi*50*t) + np.cos(2*np.pi*115*t) + np.cos(2*np.pi*230*t) + np.cos(2*np.pi*400*t) + np.cos(2*np.pi*900*t)    # Rx_signal

snr_dB = 10            #SNR in dB
snr = pow(10,snr_dB/10)    #linear SNR
signal_power = pow(np.linalg.norm(Rx_signal),2)/len(Rx_signal)    #modulated signal power(신호벡터크기 계산)
noise_power = signal_power/snr  #noise power
noise_std = np.sqrt(noise_power)    #noise standard deviation
noise = noise_std*np.random.normal(size = (len(Rx_signal))) # awgn noise

RX_result = noise + Rx_signal   # Sum sig nal = RX_signal + noise

'''
Plot Rx_signal & PSD(power spectrum dencity)
'''
NFFT = len(RX_result)
# plt.figure()
# plt.subplot(2,1,1)
# plt.plot(t, RX_result);plt.grid();plt.title('Sonar LOFAR Algoritum Receive Siganl(SNR 10dB)');plt.xlabel('Time(sec)');plt.ylabel('Amplitude')
# # plt.tight_layout()
# plt.subplot(2,1,2)
# # plt.figure()
# plt.psd(RX_result, NFFT, Fs)
# plt.xlim(0,1e3)
# plt.tight_layout()

'''
Spectrogram with LOFAR Algoritum 
window = hanning window
nfft = 8192(Bin Data), 주파수를 몇단계로 분활 할 것인지의 대한 변수 값
nperseg = window size(8192)
noverlap = 50%
'''
#STFT_f : frequency vector, STFT_t: time vector, STFT_Zxx:  N X M matrix
STFT_f, STFT_t, STFT_Zxx = signal.spectrogram(RX_result, Fs, window = 'hann',nfft=2**13, nperseg=512, noverlap=(512)/8)

# TPM(time pass mean) 결과값을 위한 matrix generate
a,b = np.shape(STFT_Zxx)
R = np.zeros((a,b))
# TPM(time pass mean) algorithum
for p in range(len(STFT_t)):    #전체 시간 프렘임의 대한 계산
    ST_result = STFT_Zxx[:,p]   # 전체 시간 프렘임에서 Indexing 하여 한 프렘임 씩 계산 진행
    M = (len(ST_result ) - 1) / 2   # window size = (k - 1)/2, k = 한 프렘이의 길이
    print(p)
    for i in range(len(ST_result)):
        #범위 평균을 구하기 위한 계산 식
        # 해당 index - window size 값이 
        if i - M <= 0:
            start = 0
        elif i-M > 0:
            start = int(i-M)
        if i+M > len(ST_result):
            end = len(ST_result)
        elif i+M <= len(ST_result):
            end = int(i + M)
        sum = 0
        max = 0
        for k in range(start, end):
            sum = sum + ST_result[k]
            max += 1
        me = sum/ max
        # R[i,p] = ST_result[i] / me
        if ST_result[i] / me < 70:
            R[i,p] = -(ST_result[i] / me)
        elif ST_result[i] / me > 70:   
            R[i,p] = ST_result[i] / me


plt.figure()
plt.pcolormesh(STFT_t,STFT_f,STFT_Zxx, cmap='gist_gray',shading='gouraud');plt.ylim(0,1.2e3)
plt.colorbar(format='%.f dB')

plt.figure()
plt.pcolormesh(STFT_t,STFT_f,R,cmap='gist_gray',shading='gouraud');plt.ylim(0,1.2e3)
plt.colorbar(format='%.f dB')

print(np.shape(R))
plt.show()


