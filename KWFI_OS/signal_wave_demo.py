# '''
# simulate a sinusoidal signal with given sampling rate
# '''
# 
# import numpy as np
# import matplotlib.pyplot as plt #library for plotting
# from signalgen import sine_wave
# 
# f = 10 # frequency = 10Hz
# overSampRate = 30 # oversammpling rate
# phase = 1/3*np.pi # phase shift in radians
# nCy1 = 5 # desired number of cycles of the sine wave
# 
# (t,g) = sine_wave(f,overSampRate,phase,nCy1)
# 
# plt.plot(t,g); plt.title('sine wave f='+str(f)+'Hz'); plt.xlabel('Time(s)'); plt.ylabel('Amplitude')
# plt.show()
# 
# 
# 
# '''
# Generate a square wave with given samplig rate
# '''
# 
# import numpy as np
# import matplotlib.pyplot as plt #library for plotting
# from signalgen import *
# from scipy import signal
# 
# f = 10 # frequency = 10Hz
# overSampRate = 30 # oversammpling rate
# nCy1 = 5 # desired number of cycles of the sine wave
# 
# (t,g) = square_wave(f,overSampRate,nCy1)
# plt.figure(1)
# plt.plot(t,g); plt.title('square wave f='+str(f)+'Hz'); plt.xlabel('Time(s)'); plt.ylabel('Amplitude')
# #plt.show()
# 
# fs = overSampRate * f
# t1 = np.arange(start = 0, stop = nCy1*1/f, step = 1/fs)
# g1 = signal.square(2*np.pi*f*t1, duty = 0.2)
# plt.figure(2)
# plt.plot(t1,g1);plt.title('square wave f='+str(f)+'Hz'); plt.xlabel('Time(s)'); plt.ylabel('Amplitude')
# plt.show()

# '''
# Generate isolated rectangular pulse with the following parameters
# '''
# import numpy as np
# import matplotlib.pyplot as plt #library for plotting
# from signalgen import *
# 
# A = 1; fs = 500; T = 0.2;
# (t,g) = rect_pulse(A,fs,T)
# 
# plt.plot(t,g); plt.title('Rectangular pylse width ='+str(T)+'s')
# plt.xlabel('Time(s)');plt.ylabel('Amplitude')
# plt.show()


# '''
# Generate isolated Gaussian pulse with the following parameters
# '''
# import numpy as np
# import matplotlib.pyplot as plt #library for plotting
# from signalgen import *
# 
# fs = 80; sigma = 0.1;
# (t,g) = gaussian_pulse(fs,sigma)
# 
# plt.plot(t,g); plt.title('Gaussian pulse ='+str(sigma)+'s')
# plt.xlabel('Time(s)');plt.ylabel('Amplitude')
# plt.show()

'''
Generating and plotting a chirp signal
'''
import numpy as np
import matplotlib.pyplot as plt #library for plotting
from scipy.signal import chirp

fs = 500 # sampling frequency in Hz
t = np.arange(start = 0, stop = 1, step = 1/fs)
g = chirp(t, f0= 1, t1 = 0.5, f1 = 20, phi = 0, method = 'linear')

plt.plot(t,g); plt.title('chirp Signal')
plt.xlabel('Time(s)');plt.ylabel('Amplitude')
plt.show()
