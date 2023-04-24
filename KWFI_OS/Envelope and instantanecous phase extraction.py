#%%
'''
Date: 2021.08.19
Title: Envelope and instantanecous phase extraction
By: Kang Jin Seong
'''

'''
Demonstrate extraction of instantaneous amplitude and phse from
the analytic signal constructed from a real-valued modulated signal
'''

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


from scipy.fftpack import fft, ifft, fftshift, ifftshift
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import chirp


fs = 600 # sampling frequency in Hz
t = np.arange(start = 0, stop = 1, step = 1/fs) #time base
a_t = 1+0.7*np.sin(2*np.pi*3*t) # information signal
c_t = chirp(t, f0 = 20, t1 = t[-1], f1 = 80, phi = 0, method = 'linear')
x = a_t * c_t # modulated signal

fig, (ax1,ax2) = plt.subplots(nrows = 2, ncols = 1)
ax1.plot(x) # plot the modulated signal
z = analytic_signal(x) # form the analytical signal
inst_amplitude = abs(z) # envlope extraction
inst_phase = np.unwrap(np.angle(z)) # inst phase
inst_freq = np.diff(inst_phase)/(2*np.pi)*fs # inst frequency

#Regenerate the carrier from the instantaneous phase
extracted_carrier = np.cos(inst_phase)
ax1.plot(inst_amplitude,'r') # overlay the extracted envelope
ax1.set_title('Modulated signal and extracted envelope')
ax1.set_xlabel('n');ax1.set_ylabel(r'x(t) and $|z(t)|$')
ax2.plot(extracted_carrier)
ax2.set_title('Extracted carrier or TFS')
ax2.set_xlabel('n');ax2.set_ylabel(r'$cos[\omega(t)]$')
fig.tight_layout()
fig.savefig(r'C:\Users\USER\Desktop\DSP_python\Envelope and instantanecous phase extraction(Hilbert Transform).png')
fig.show()
t1 = t[-1]
# %%
