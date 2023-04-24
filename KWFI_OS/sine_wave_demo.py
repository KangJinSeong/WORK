'''
simulate a sinusoidal signal with given sampling rate
'''

import numpy as np
import matplotlib.pyplot as plt #library for plotting
from signalgen import sine_wave

f = 10 # frequency = 10Hz
overSampRate = 30 # oversammpling rate
phase = 1/3*np.pi # phase shift in radians
nCy1 = 5 # desired number of cycles of the sine wave

(t,g) = sine_wave(f,overSampRate,phase,nCy1)

plt.plot(t,g); plt.title('sine wave f='+str(f)+'Hz'); plt.xlabel('Time(s)'); plt.ylabel('Amplitude')
plt.show()