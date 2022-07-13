'''
Date: 2022.02.10
Title: Sonar LOFAR Algorithum test
By: Kang Jin Seong
'''

#%%
from cmath import log10
from scipy.fftpack import fft, ifft, fftshift, ifftshift
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

Fs = 192e3
t = np.arange(start = 0, stop = 10, step = 1/Fs)

Rx_signal = np.cos(2*np.pi*50*t) + np.cos(2*np.pi*115*t) + np.cos(2*np.pi*230*t) + np.cos(2*np.pi*400*t) + np.cos(2*np.pi*900*t)

snr_dB = 10            #SNR in dB
snr = pow(10,snr_dB/10)    #linear SNR
signal_power = pow(np.linalg.norm(Rx_signal),2)/len(Rx_signal)    #modulated signal power(신호벡터크기 계산)
noise_power = signal_power/snr  #noise power
noise_std = np.sqrt(noise_power)    #noise standard deviation
noise = noise_std*np.random.normal(size = (len(Rx_signal))) # awgn noise

RX_result = noise + Rx_signal
NFFT = len(RX_result)
plt.figure()
# plt.subplot(2,1,1)
plt.plot(t, RX_result);plt.grid();plt.title('Sonar LOFAR Algoritum Receive Siganl(SNR 10dB)');plt.xlabel('Time(sec)');plt.ylabel('Amplitude')
plt.tight_layout()
# plt.subplot(2,1,2)
plt.figure()
plt.psd(RX_result, NFFT, Fs)
plt.xlim(0,1e3)
plt.tight_layout()



welch_f, Pxx_den = signal.welch(RX_result, Fs, nperseg=NFFT,scaling='spectrum')

Window_result_signal = np.real(NFFT*ifft(Pxx_den,NFFT))

result = [0] * len(t)

for i in range(len(Window_result_signal)):
    if i >= len(Window_result_signal) / 2: 
        result[i] = Window_result_signal[i-(int(len(Window_result_signal)/2))]
    elif i < len(Window_result_signal) / 2:
        result[i] = Window_result_signal[(int(len(Window_result_signal)/2)) + i]
result = np.array(result)
# plt.figure()
# plt.semilogy(welch_f, Pxx_den);plt.grid();plt.xlim(0,1e3)

# plt.figure()
# plt.plot(t,result);plt.grid()

# STFT_f, STFT_t, STFT_Zxx = signal.spectrogram(RX_result, Fs, window = 'hann',nfft=2**13, nperseg=2**13, noverlap=(2**13)/2)

# a,b = np.shape(STFT_Zxx)

# R = np.zeros((a,b))

# for p in range(len(STFT_t)):
#     ST_result = STFT_Zxx[:,p]
#     M = (len(ST_result ) - 1) / 2
#     print(p)
#     for i in range(len(ST_result)):
#         if i - M == 0:
#             start = 0
#         elif i-M != 0:
#             start = int(i-M)
#         if i+M > len(ST_result):
#             end = len(ST_result)
#         elif i+M <= len(ST_result):
#             end = int(i + M)
#         sum = 0
#         max = 0
#         for k in range(start, end):
#             sum = sum + ST_result[k]
#             max += 1
#         me = sum/ max
#         if ST_result[i] / me < 150:
#             R[i,p] = 0
#         elif ST_result[i] / me > 150:   
#             R[i,p] = ST_result[i] / me


# plt.figure()
# plt.pcolormesh(STFT_t,STFT_f,STFT_Zxx, cmap='gist_gray',shading='gouraud');plt.ylim(0,1.2e3)
# plt.colorbar(format='%.f dB')

# plt.figure()
# plt.pcolormesh(STFT_t,STFT_f,R,cmap='gist_gray',shading='gouraud');plt.ylim(0,1.2e3)
# plt.colorbar(format='%.f dB')

# print(np.shape(R))
plt.show()

# %%
