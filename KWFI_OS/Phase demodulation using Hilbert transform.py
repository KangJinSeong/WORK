
'''
Date: 2021.08.20
Title: Phase demodulation using Hilbert transform
By: Kang Jin Seong
'''

'''
Demonstrate simple Phase Demodulation using Hilbert transform
'''

from scipy.fftpack import fft, ifft, fftshift, ifftshift
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import chirp, hilbert

fc = 210 # carrier frequency
fm = 10 # frequency of modulating signal
alpha = 1 # amplitude of modulating signal
theta = np.pi/4 # phase offset of modulating signal
beta = np.pi/5 # constant carrier phase offset

#SET true if receiver knows carrier frequenct & phase offset

receiverKnowsCarrier = False

fs = 8*fc # sampling frequency
duration = 0.5 # duration of the signal
t = np.arange(start = 0, stop = duration , step = 1/fs) # time base

#phase Modulation
m_t = alpha * np.sin(2*np.pi*fm*t+theta) # modulating signal
x = np.cos(2*np.pi*fc*t + beta+ m_t) # modulated signal

fig1, (ax1,ax2) = plt.subplots(nrows = 2, ncols = 1)
ax1.plot(t,m_t) # plot modulating signal
ax1.set_title('Modulating signal')
ax1.set_xlabel('t'); ax1.set_ylabel('x(t)');
ax2.plot(t,x) # plot modulated signal
ax2.set_title('Modulated signal')
ax2.set_xlabel('t');ax2.set_ylabel('x(t)')
fig1.tight_layout()
fig1.show()
fig1.savefig(r'C:\Users\USER\Desktop\DSP_python\Phase modulation-modulating signal and modulated(transmitted)signal.png')


#Add AWGN noise to the transmitted signal
mu = 0; sigma = 0.1 # noise mean and sigma
n = mu + sigma*np.random.normal(len(t)) #Awgn noise
r = x + n # noisy received signal

#Demodulation of the noisy phase moduation signal
z = hilbert(r) # form the analytical signal from the received freq/phase perfectly
inst_phase = np.unwrap(np.angle(z)) # instaneous phase

if receiverKnowsCarrier: # If receiver knows the carrier freq/phase perfectly
    offsetTerm = 2*np.pi*fc*t+beta
else: #elsem estimate the subtrcation term
    p = np.polyfit(x = t, y = inst_phase, deg = 1) #linear fit instantaneous phase
    #re-evaluate the offset term using the fitted values
    estimated = np.polyval(p,t)
    offsetTerm = estimated

demodulated = inst_phase-offsetTerm

fig2, (ax3) = plt.subplots(nrows = 1, ncols = 1)
ax3.plot(t,demodulated) #demodulated signal
ax3.set_title('Demodulated signal')
ax3.set_xlabel('n')
ax3.set_ylabel(r'$\hat{m(T)}$');
fig2.tight_layout()
fig2.show()
fig2.savefig(r'C:\Users\USER\Desktop\DSP_python\Demodulated signal.png')

plt.show()