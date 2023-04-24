import DSSS
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft, fftshift, ifftshift
import numpy as np
from matplotlib import font_manager, rc
font_path = "C:/Windows/Fonts/gulim.ttc"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

Fs = 100e3
t = np.arange(0,0.1,1/Fs)
y = np.cos(2*np.pi*1e3*t)
y1 = np.cos(2*np.pi*(1e3/Fs)*t)
plt.plot(t,y)
plt.plot(t,y1,'g-')
plt.show()