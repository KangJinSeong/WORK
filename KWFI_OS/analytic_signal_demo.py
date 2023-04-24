'''
Date: 2021.08.19
Title: Investigate components of an analytic signal
By: Kang Jin Seong
'''
from scipy.fftpack import fft, ifft, fftshift, ifftshift
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import chirp

def analytic_signal(x):
    '''
    Generate analytic signal using frequency domain approach
    Parameters:
        x : Signal data. Must be real
    Returns:
        z : Analytic signal of x
    '''
    from scipy.fftpack import fft,ifft
    N = len(x)
    X = fft(x,N)
    Z = np.hstack((X[0], 2*X[1:N//2],X[N//2], np.zeros(N//2-1)))
    z = ifft(Z,N)
    return z


t = np.arange(start = 0, stop = 0.5, step = 0.001) #time base
x = np.sin(2*np.pi*10*t) # real-valued f = 10Hz

fig, (ax1,ax2) = plt.subplots(nrows = 2, ncols = 1)
ax1.plot(t,x) # plot the original signal
ax1.set_title('x[n] - real-valued signal')
ax1.set_xlabel('n');ax1.set_ylabel('x[n]')

z = analytic_signal(x) # construct analytic signal

ax2.plot(t, np.real(z), 'k', label = 'Real(z[n])')
ax2.plot(t, np.imag(z), 'r', label = 'Imag(z[n])')
ax2.set_title('Components of Analytic signal')
ax2.set_xlabel('n')
ax2.set_ylabel(r'$z_r[n]$ and $z_i[n]$')
ax2.legend()
fig.tight_layout()
fig.savefig('/home/pi/DSP_python/Investigate components of an analytic signal.png')
fig.show()
