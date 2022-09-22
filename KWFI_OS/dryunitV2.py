#%%
'''
Date: 2021.09.01
Title: Dry Unit v2.0
By: Kang Jin Seong
'''
import pandas as pd
from scipy.fftpack import fft, ifft, fftshift, ifftshift
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import chirp, hilbert
from scipy import signal
from scipy.signal import upfirdn
from queue import Queue



fs = 32000*8*8 # sampling frequency


'''
Chirpping signal generate
'''

t = np.arange(start = 0, stop = 0.128, step = 1/fs) #Chirp time base
g1 = chirp(t, f0= 30000, t1 = 0.128, f1 = 34000, method = 'linear') # UP-chirpping signal
g2 = chirp(t, f0= 34000, t1 = 0.128, f1 = 30000, method = 'linear') # DOWN-chirpping signal

zero_s = (np.zeros((1,int(0.1*fs))).tolist())[0]
zero_e = (np.zeros((1,int(0.2*fs))).tolist())[0]

zero1_s = (np.zeros((1,int(0.15*fs))).tolist())[0]

# plt.figure()
# plt.plot(t,g1)

NFFT = len(t)
f1 = np.arange(start = -NFFT/2, stop = NFFT/2)*(fs/NFFT)
M1 = fftshift(fft(g1,NFFT))/NFFT

# plt.figure()
# plt.plot(f1,M1)
# plt.xlim(-50000, 50000)
# plt.show()

'''
receive signal generate
'''
r_ch1 = []
r_ch1.extend(zero_s)
r_ch1.extend(g1) #0
r_ch1.extend(g2) #1
r_ch1.extend(g1) #0
r_ch1.extend(g1) #0
r_ch1.extend(g2) #1
r_ch1.extend(zero_e)

r_ch2 = []
r_ch2.extend(zero1_s)
r_ch2.extend(g1)
r_ch2.extend(g2)
r_ch2.extend(g1)
r_ch2.extend(g1)
r_ch2.extend(g2)
r_ch2.extend(zero1_s)

N = len(r_ch1)
num_frame = 10

r_ch1 = np.array(r_ch1)
r_ch2 = np.array(r_ch2)


'''
Data Queue 선언
'''
ch1_ADC_Q = Queue()
ch2_ADC_Q = Queue()



def ADC():
    for i in range(0,num_frame):
        data1 = r_ch1[i*192512:(192512)*(i+1)]
        # data2 = r_ch2[i*1310719:(1310719)*(i+1)]
        ch1_ADC_Q.put(data1)
        # ch2_ADC_Q.put(data2)

def pro_process():
    global X1_ch1, X2_ch1, X1_ch2, X2_ch2
    X1_ch1 = []
    X2_ch1 = []
    X1_ch2 = []
    X2_ch2 = []
    for i in range(0,num_frame):
        ADC_data1 = ch1_ADC_Q.get()
        # ADC_data2 = ch2_ADC_Q.get()

        y1_ch1 = signal.correlate(ADC_data1,g1)
        y2_ch1 = signal.correlate(ADC_data1,g2)

        # y1_ch2 = signal.fftconvolve(ADC_data2,g1)
        # y2_ch2 = signal.fftconvolve(ADC_data2,g2)

        X1_ch1.extend(y1_ch1)
        X2_ch1.extend(y2_ch1)

        # X1_ch2.extend(y1_ch2)
        # X2_ch2.extend(y2_ch2)

    X1_ch1 = np.array(X1_ch1)
    X2_ch1 = np.array(X2_ch1)
    # X1_ch2 = np.array(X1_ch2)
    # X2_ch2 = np.array(X2_ch2) 
 
ADC()
pro_process()

r_t = np.arange(start = 0, stop = len(X1_ch1))*1/fs

X_ch1 = abs(X1_ch1) - abs(X2_ch1)
# X_ch2 = abs(X1_ch2) - abs(X2_ch2)

X_ch1 = X_ch1/np.max(X_ch1)
# X_ch2 = X_ch2/np.max(X_ch2)

plt.figure()
plt.plot(r_t, X_ch1)

plt.figure()
plt.plot(r_t, abs(X1_ch1),'k', r_t, abs(X2_ch1),'r')
plt.show()

# '''
# Signal porcess 
# '''
# alpha = 0

# y_ch1 = pd.Series(X_ch1)
# ma_y_ch1 = y_ch1.rolling(160).mean()
# ma_y_ch1 = ma_y_ch1[159:]
# yt_p = np.max(ma_y_ch1 + (np.max(ma_y_ch1) - np.min(ma_y_ch1) + alpha))
# yt_n = np.min(ma_y_ch1 + (np.max(ma_y_ch1) - np.min(ma_y_ch1) + alpha))


# Peak_ind0, _ = signal.find_peaks(ma_y_ch1, height= yt_p , distance = len(g1))
# Peak_ind1, _ = signal.find_peaks(-ma_y_ch1, height= -yt_n , distance = len(g2))

# print(len(y_ch1))
# print(len(ma_y_ch1))

# print(yt_p)
# print(yt_n)

# print('peak_ind0 = ', Peak_ind0)
# print('peak_ind1 = ', Peak_ind1)

# plt.figure()
# plt.plot(ma_y_ch1)
# plt.show()





# %%
