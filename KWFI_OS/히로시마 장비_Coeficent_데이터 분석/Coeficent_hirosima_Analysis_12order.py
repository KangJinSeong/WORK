'''
Date: 2023.05.18
Title: 히로시마 장비 Coeficent 분석 자료
By: Kang Jin Seong
'''


import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fftpack import fft, fftshift
from scipy import signal
from scipy.signal import hilbert

def hl_envelopes_idx(s, dmin=1, dmax=1, split=False):
    """
    Input :
    s: 1d-array, data signal from which to extract high and low envelopes
    dmin, dmax: int, optional, size of chunks, use this if the size of the input signal is too big
    split: bool, optional, if True, split the signal in half along its mean, might help to generate the envelope in some cases
    Output :
    lmin,lmax : high/low envelope idx of input signal s
    """

    # locals min      
    lmin = (np.diff(np.sign(np.diff(s))) > 0).nonzero()[0] + 1 
    # locals max
    lmax = (np.diff(np.sign(np.diff(s))) < 0).nonzero()[0] + 1 
    
    if split:
        # s_mid is zero if s centered around x-axis or more generally mean of signal
        s_mid = np.mean(s) 
        # pre-sorting of locals min based on relative position with respect to s_mid 
        lmin = lmin[s[lmin]<s_mid]
        # pre-sorting of local max based on relative position with respect to s_mid 
        lmax = lmax[s[lmax]>s_mid]

    # global min of dmin-chunks of locals min 
    lmin = lmin[[i+np.argmin(s[lmin[i:i+dmin]]) for i in range(0,len(lmin),dmin)]]
    # global max of dmax-chunks of locals max 
    lmax = lmax[[i+np.argmax(s[lmax[i:i+dmax]]) for i in range(0,len(lmax),dmax)]]
    
    return lmin,lmax


fs = 64e3
fs1, data = wavfile.read('K6_M12Q2R3.wav')

t = np.arange(start = 0, stop =len(data))*(1/fs)

NFFT = len(data)
f = np.arange(start = -NFFT/2, stop = NFFT/2)*(fs/NFFT) 
X = fftshift(fft(data, len(data))) * (1/NFFT)

# lmin, lmax = hl_envelopes_idx(X, dmin = 30, dmax= 30)




plt.figure()
plt.plot(f, X)


y = np.cos(2*np.pi*5e3*t)

result = (data * y)
sos = signal.butter(10, [2500], 'low', fs=fs, output='sos')
filtered = signal.sosfilt(sos, result)
yy = [i if i>0 else 0 for i in filtered]
coefi_result = [1 if i>2000 else 0 for i in yy]

start_index = int(2.0006*fs) + 3

plt.figure()
plt.plot(t[int(2*fs):int(2*fs)+1000], data[int(2*fs):int(2*fs)+1000])




d_t = t[start_index:start_index+1000]
d_coefi_result = coefi_result[start_index:start_index+1000]

n_t = (1/(5e3))*2
l_t = int(n_t * fs)


plt.figure()
plt.stem(d_t,d_coefi_result)
plt.figure()

plt.stem(d_t[0::l_t],d_coefi_result[0::l_t], linefmt='grey', markerfmt='D')

answer = coefi_result[start_index::l_t]

pre_data = 13
c_data = 4096

last_data = (pre_data + c_data) * 3

# print(len(answer), last_data)
RESULT  = answer[:-253]

# plt.figure()
# plt.stem(RESULT)

COEF = RESULT[:4096]
print(len(COEF)) 

plt.figure()
plt.stem(COEF)

with open('Coeficent_히로시마_12order.txt', 'w') as f:
    for i in COEF:
        f.write(str(i)+'\r\n')
plt.show()















