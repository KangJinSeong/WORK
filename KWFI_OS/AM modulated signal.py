#%%
'''
Date: 2021.08.25
Title: Amplitude modulating and modulated signal(DSB-SC)
By: Kang Jin Seong
'''

from scipy.fftpack import fft, ifft, fftshift, ifftshift
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import chirp, hilbert
from scipy import signal
from itertools import chain

'''
Modulated signal
'''

fs = (1/0.001)

snr = 20
snr_lin = pow(10,snr/10)

def triangle_signal():
    y = []
    y1 = list(signal.triang((0.1*fs)))
    y2 = (np.zeros((1,int(0.05*fs))).tolist())[0]
    y.extend(y2)
    y.extend(y1)
    y.extend(y2)
    return y


m_y = triangle_signal()
t = np.arange(start = -0.1, stop = 0.1, step = 1/fs)

Sm_c = np.cos(2*np.pi*250*t)
Sm_y = Sm_c * m_y

fig1, (ax1, ax2) = plt.subplots(nrows = 2, ncols = 1)
ax1.plot(t,m_y);ax1.set_title('Message signal');ax1.set_xlabel('Time(s)')
ax2.plot(t,Sm_y);ax2.set_title('Modulated signal');ax2.set_xlabel('Time(s)')
fig1.tight_layout()
# fig1.show()

NFFT = len(Sm_y)

M_Y = fftshift(fft(m_y, NFFT))/NFFT  # 1/NFFT : Scaling
SM_Y = fftshift(fft(Sm_y, NFFT))/NFFT
f = np.arange(start = -NFFT/2, stop = NFFT/2)*fs/NFFT

fig2, (ax3,ax4) = plt.subplots(nrows = 2, ncols = 1)
ax3.plot(f,abs(M_Y));ax3.set_title('Spectrum of the message signal');ax3.set_xlabel('Frequency(Hz)')
ax4.plot(f,abs(SM_Y));ax4.set_title('Spectrum of the modulated signal');ax4.set_xlabel('Frequency(Hz)')
fig2.tight_layout()
# fig2.show()

# Add AWGN noise to the transmitted signal
mu = 0; sigma = 10 # noise mean and sigma
signal_power = pow(np.linalg.norm(m_y),2/len(t))
noise_power = signal_power/snr_lin
noise_std = np.sqrt(noise_power)

n = noise_std*np.random.normal(size = (len(t))) # awgn noise
r = Sm_y + n
R = fftshift(fft(r, NFFT))/NFFT

fig3, (ax5, ax6) = plt.subplots(nrows = 2, ncols = 1)
ax5.plot(t,n);ax5.set_title('noise sample');ax5.set_xlabel('Time(s)')
ax6.plot(t,r);ax6.set_title('signal and noise');ax6.set_xlabel('Time(s)')
fig3.tight_layout()
# fig3.show()

fig4, (ax7, ax8) = plt.subplots(nrows = 2, ncols = 1)
ax7.plot(f,abs(SM_Y));ax7.set_title('signal spectrum');ax7.set_xlabel('Frequency(Hz)')
ax8.plot(f,abs(R));ax8.set_title('signal and noise spectrum');ax8.set_xlabel('Frequency(Hz)')
fig4.tight_layout()
# fig4.show()

'''
Demodulated signal
'''
def low_pass_filter():
    y = []
    y1 = (np.zeros((1,int(400*NFFT/fs))).tolist())[0]
    y2 = (np.ones((1,int(200*NFFT/fs))).tolist())[0]
    y.extend(y1)
    y.extend(y2)
    y.extend(y1)
    return y

r = Sm_y # + n : add noise
r_y = r * Sm_c
R_Y = fftshift(fft(r_y, NFFT))/NFFT

fil = low_pass_filter()

fig5, (ax9, ax10, ax11) = plt.subplots(nrows = 3, ncols = 1)
ax9.plot(f,abs(M_Y));ax9.set_title('Spectrum of the message signal');ax9.set_xlabel('Frequency(Hz)')
ax10.plot(f,abs(R));ax10.set_title('Spectrum of the Received signal');ax10.set_xlabel('Frequency(Hz)')
ax11.plot(f,abs(R_Y));ax11.set_title('Spectrum of the Mixer Output');ax11.set_xlabel('Frequency(Hz)')
fig5.tight_layout()
fig5.show()

DE_Y = R_Y * fil

fig6, (ax12, ax13, ax14) = plt.subplots(nrows = 3, ncols = 1)
ax12.plot(f,abs(R_Y));ax12.set_title('Spectrum of the Mixer Output');ax12.set_xlabel('Frequency(Hz)')
ax13.plot(f,fil);ax13.set_title('Lowpass filter characteristic');ax13.set_xlabel('Frequency(Hz)')
ax14.plot(f,abs(DE_Y));ax14.set_title('Spectrum of the Demodulator Output');ax14.set_xlabel('Frequency(Hz)')
fig6.tight_layout()
# fig6.show()

De_y = NFFT * ifft(ifftshift(DE_Y),NFFT)
fig7, (ax15, ax16) = plt.subplots(nrows = 2, ncols = 1)
ax15.plot(t,m_y);ax15.set_title('Message signal');ax15.set_xlabel('Time(s)')
ax16.plot(t,np.real(De_y));ax16.set_title('The Demodulator Ouput');ax15.set_xlabel('Time(s)')
fig7.tight_layout()
# fig7.show()




# %%
