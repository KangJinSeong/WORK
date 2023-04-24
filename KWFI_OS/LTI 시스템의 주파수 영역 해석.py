'''
Date: 2022.11.09
Title: 
By: Kang Jin Seong
'''

from scipy.fftpack import fft,fftshift,ifft,ifftshift
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

df = 0.01
fs = 10

t = np.arange(-5, 5, 1/fs)

x = np.zeros(len(t), int)
x[31:41] = 2*np.ones(10)
x[41:61] = 2-2*np.cos(0.5*np.pi*t[41:61])
x[61:71] = 2*np.ones(10)
x[71:91] = 4-t[71:91]

NFFT = len(t)
X = fftshift(fft(x,NFFT))
f = np.arange(start = -NFFT/2, stop = NFFT/2)*fs/NFFT
df1 = fs/NFFT

fig1, (ax1, ax2) = plt.subplots(nrows = 2, ncols = 1)
ax1.plot(t, x)
ax2.plot(f, abs(X)/fs)
plt.tight_layout()
# plt.show()

H = []
# H.extend(np.ones(int(np.ceil(1.5/df1))))
# H.extend(np.zeros(int(len(X) - 2*np.ceil(1.5/df1))))
# H.extend(np.ones(int(np.ceil(1.5/df1))))
H.extend(np.zeros(int(np.ceil(1.5/df1))))
H.extend(np.ones(int(len(X) - 2*np.ceil(1.5/df1))))
H.extend(np.zeros(int(np.ceil(1.5/df1))))


plt.figure()
plt.plot(f,H)

H = np.array(H)

Y = H * X

y1 = ifft(Y)
plt.figure()
plt.plot(t, abs(y1))
plt.show()


