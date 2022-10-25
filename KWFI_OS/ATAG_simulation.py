'''
Date: 2022.10.24
Title: 어구자동식별모니터링 시스템 음향태그 Linkbudget 시뮬레이션
By: Kang Jin Seong
'''

from scipy.fftpack import fft, ifft, fftshift, ifftshift
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import chirp
from scipy import signal

fs = 192000 # sampling frequency
nCy1 = 6144# Number of cycles of the sinewave

tt = np.arange(start = 0, stop = nCy1/fs, step = 1/fs)
g = 0.061*chirp(tt, f0= 30000, t1 = nCy1/fs, f1 = 34000, method = 'linear')

fig1, (ax1,ax2) = plt.subplots(nrows = 2, ncols = 1)
ax1.plot(tt,g);ax1.set_title('Chirp signal ')
ax2.psd(g,len(g),fs); ax2.set_title('ADC channel #1 Power Spectral density') # plt.psd(x, NFFT, FS)
fig1.tight_layout()
# fig1.show()
# plt.show()

snr_dB = 6           #SNR in dB
snr = pow(10,snr_dB/10)    #linear SNR
signal_power = pow(np.linalg.norm(g),2)/len(g)    #modulated signal power(신호벡터크기 계산)
noise_power = signal_power/snr  #noise power
noise_std = np.sqrt(noise_power)    #noise standard deviation
noise = noise_std*np.random.normal(size = (len(g))) # awgn noise

# RX_result = noise + g   # Sum sig nal = RX_signal + noise

NLshipping = 70 - 20*np.log(32e3/100)
NLsupf = 64.5 - 17*np.log(32e3/1000)# seastate : 3

RX_result = noise + g + NLshipping + NLsupf
RX_result = pow(10,RX_result/20) 
fig2, (ax3,ax4) = plt.subplots(nrows = 2, ncols = 1)
ax3.plot(tt,RX_result);ax3.set_title('Chirp signal + SNR 6dB Noise Signal+ Traffic Noise + Surface noise ')
ax4.psd(RX_result,len(RX_result),fs); ax4.set_title('ADC channel #1 Power Spectral density') # plt.psd(x, NFFT, FS)
fig2.tight_layout()
# plt.show()


y1_ch1 = signal.correlate(RX_result,g, method= 'fft')
y2_ch1 = (y1_ch1 - np.min(y1_ch1)) / (np.max(y1_ch1) - np.min(y1_ch1))
y1_ch1_t = np.arange(0,len(y1_ch1))
fig3, (ax3,ax4) = plt.subplots(nrows = 2, ncols = 1)
ax3.plot(y1_ch1_t,y1_ch1);ax3.set_title('Convolution Result ADC channel(FFT) #1');ax3.set_xlabel('number of sample(n)')
ax4.plot(y1_ch1_t,y2_ch1,'r'); ax4.set_title('Min-Max Normalization')
ax4.set_xlabel('number of sample(n)') # plt.psd(x, NFFT, FS)
fig3.tight_layout()

plt.show()
