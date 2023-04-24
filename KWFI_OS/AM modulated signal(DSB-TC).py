#%%
'''
Date: 2021.08.25
Title: Amplitude modulating and modulated signal(DSB-TC)
By: Kang Jin Seong
'''

from scipy.fftpack import fft, ifft, fftshift, ifftshift
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import chirp, hilbert

'''
Modulated signal
'''

fs = (1/0.001)

snr = 20
snr_lin = pow(10,snr/10)

def mt_signal():
    y = []
    y1 = (np.ones((1,int(0.05*fs))).tolist())[0]
    y2 = ((np.ones((1,int(0.05*fs)))*-2).tolist())[0]
    y3 = (np.zeros((1,int(0.05*fs))).tolist())[0]
    y.extend(y1)
    y.extend(y2)
    y.extend(y3)
    return y

m_y = mt_signal()
m_y = np.array(m_y)
m_y_n = m_y/np.max(abs(m_y))
t = np.arange(start = 0, stop = 0.15, step = 1/fs)
Sm_c = np.cos(2*np.pi*250*t)
Sm_y = (1+0.85*m_y_n)*Sm_c

fig1, (ax1, ax2) = plt.subplots(nrows = 2, ncols = 1)
ax1.plot(t,m_y);ax1.set_title('Message signal');ax1.set_xlabel('Time(s)')
ax2.plot(t,Sm_y);ax2.set_title('Modulated signal');ax2.set_xlabel('Time(s)')
fig1.tight_layout()
fig1.show()

NFFT = len(t)
f = np.arange(start = -NFFT/2, stop = NFFT/2)*fs/NFFT

M_Y = fftshift(fft(m_y,NFFT))/NFFT
SM_Y = fftshift(fft(Sm_y,NFFT))/NFFT

fig2, (ax3, ax4) = plt.subplots(nrows = 2, ncols = 1)
ax3.plot(f,abs(M_Y));ax3.set_title('Spectrum of the message signal');ax3.set_xlabel('Frequency(Hz)')
ax4.plot(f,abs(SM_Y));ax4.set_title('Spectrum of the modulated signal');ax4.set_xlabel('Frequency(Hz)')
fig2.tight_layout()
# fig2.show()

z = hilbert(Sm_y)
inst_amplitude = abs(z)
Z = fftshift(fft(z,NFFT))/NFFT

fig3, (ax4, ax5) = plt.subplots(nrows = 2, ncols = 1)
ax4.plot(t,Sm_y);ax4.set_title('Modulated signal');ax4.set_xlabel('Time(s)')
ax5.plot(t,inst_amplitude);ax5.set_title('Envelope of the modulated signal');ax5.set_xlabel('Time(s)')
fig3.tight_layout()
fig3.show()

fig4, (ax5, ax6) = plt.subplots(nrows = 2, ncols = 1)
ax5.plot(f,abs(SM_Y));ax5.set_title('Spectrum of the modulated signal');ax5.set_xlabel('Frequency(Hz)')
ax6.plot(f,abs(Z));ax6.set_title('Spectrum of the analytic signal');ax6.set_xlabel('Frequency(Hz)')
fig4.tight_layout()
fig4.show()

dem1 =  np.max(abs(m_y)) * (inst_amplitude-1)/0.85

fig5, (ax7, ax8) = plt.subplots(nrows = 2, ncols = 1)
ax7.plot(t,m_y);ax7.set_title('Message signal');ax7.set_xlabel('Time(s)')
ax8.plot(t,dem1);ax8.set_title('Demodulated signal');ax8.set_xlabel('Time(s)')
fig5.tight_layout()
fig5.show()

# plt.show()

# %%
