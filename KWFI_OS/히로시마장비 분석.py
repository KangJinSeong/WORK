'''
Date: 2022.12.19
Title: Test
By: Kang Jin Seong
'''


import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft, fftshift, ifftshift
from matplotlib import font_manager, rc
from scipy import signal
font_path = "C:/Windows/Fonts/gulim.ttc"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)


# Fs = 192e3
# q = 5
# d_Fs = Fs/q
# t = np.arange(start = 0, stop = 1, step = 1/Fs)
# t_d = np.arange(start = 0, stop = 1, step = 1/d_Fs)
# y = np.cos(2*np.pi*5e3*t)
# y_d= signal.decimate(y, 5)

# print(len(y), len(y_d))

# plt.figure()
# plt.plot(t,y,'.-', t_d,y_d,'o-')
# # plt.xlim(0,0.001)


# yy = signal.fftconvolve(y,y)
# yy = signal.hilbert(yy)
# yy_d = signal.fftconvolve(y_d,y_d)
# yy_d = signal.hilbert(yy_d)

# plt.figure()
# plt.plot(abs(yy))
# plt.plot(abs(yy_d))
# plt.show()

Fs = 192e3
t = np.arange(0,3/5000,1/Fs)
y = np.sin(2*np.pi*5000*t + np.pi)
y1 = np.sin(2*np.pi*5000*t + 2*np.pi)
y2 = np.sin(2*np.pi*5000*t + np.pi)
y3 = np.sin(2*np.pi*5000*t + 2*np.pi)
y4 = np.sin(2*np.pi*5000*t + 3*np.pi)
y5 = np.sin(2*np.pi*5000*t + 4*np.pi)
y6 = np.sin(2*np.pi*5000*t + 4*np.pi)
y7 = np.sin(2*np.pi*5000*t + 4*np.pi)
y8 = np.sin(2*np.pi*5000*t + 3*np.pi)
result = []
result.extend(y)
result.extend(y1)
result.extend(y2)
result.extend(y3)
result.extend(y4)
result.extend(y5)
result.extend(y6)
result.extend(y7)
result.extend(y8)


t1 = np.arange(0,len(result)/Fs, 1/Fs)
yy = np.cos(2*np.pi*5000*t1)
rx = result * yy

fir = signal.firwin(255, 500/Fs, pass_zero='lowpass')
result_r = signal.lfilter(fir, [1.0],rx)

NFFT = len(result_r)
Y = fftshift(fft(rx,NFFT)*(1/NFFT))
Y1 = fftshift(fft(result,NFFT)*(1/NFFT))
Y2 = fftshift(fft(result_r,NFFT)*(1/NFFT))
y2 = ifftshift(ifft(Y2,NFFT)*NFFT)
f = np.arange(start = -NFFT/2, stop = NFFT/2)*(Fs/NFFT)

fig1, ax = plt.subplots(nrows = 3, ncols = 2)

ax[0,0].plot(t1,result)
ax[0,1].plot(f,abs(Y1))
ax[1,0].plot(t1,rx)
ax[1,1].plot(f,abs(Y))
ax[2,0].plot(t1,result_r)
ax[2,1].plot(f,abs(Y2))


moving_averages = []
i = 0
window_size = 5
while i < len(result_r) - window_size + 1:
    window_average = round(np.sum(result_r[i:i+window_size])/ window_size, 2)
    moving_averages.append(window_average)
    i += 1

plt.figure()
plt.plot(moving_averages)
plt.show()

