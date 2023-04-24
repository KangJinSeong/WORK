'''
Generate a square wave with given samplig rate
'''

import numpy as np
import matplotlib.pyplot as plt #library for plotting
from signalgen import *
from scipy import signal

f = 10 # frequency = 10Hz
overSampRate = 30 # oversammpling rate
nCy1 = 5 # desired number of cycles of the sine wave

(t,g) = square_wave(f,overSampRate,nCy1)
plt.figure(1)
plt.plot(t,g); plt.title('square wave f='+str(f)+'Hz'); plt.xlabel('Time(s)'); plt.ylabel('Amplitude')
#plt.show()

fs = overSampRate * f
t1 = np.arange(start = 0, stop = nCy1*1/f, step = 1/fs)
g1 = signal.square(2*np.pi*f*t1, duty = 0.2)
plt.figure(2)
plt.plot(t1,g1);plt.title('square wave f='+str(f)+'Hz'); plt.xlabel('Time(s)'); plt.ylabel('Amplitude')
plt.show()