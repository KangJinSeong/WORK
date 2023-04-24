#%%
'''
Date: 2021.08.30
Title: ASK,FSK,PSK modulating and modulated signal()
By: Kang Jin Seong
'''
from scipy.fftpack import fft, ifft, fftshift, ifftshift
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import chirp, hilbert
from scipy import signal
from scipy.signal import upfirdn
from scipy.stats import norm

'''
Modulation singnal - ASK, FSK, PSK
'''

# bit_N = 10
L = 16*4 # oversampling factor , L = Tb/Ts(Tb: bit period, Ts = sampling period)
# ak = np.random.randint(2, size = bit_N)
a = [0,0, 0, 0, 1, 1, 0, 1, 0, 0]
ak = np.array(a)
ask_s_bb = upfirdn(h = [1]*L, x = ak, up = L)
t = np.arange(start = 0, stop = len(ak)*L)

fc = 5000 # carrier frequencyd
fm = 800 # carrier frequency
Fs = (L*fc)/4 # sampling frequency


ask_s = ask_s_bb * np.sin(2*np.pi*fc*t/Fs)

fig1, axs = plt.subplots(nrows = 2, ncols = 2)
axs[0,0].plot(t,ask_s_bb);axs[0,0].set_title('Baseband and OOK waveforms');axs[0,0].set_xlabel('Time(s)');axs[0,0].set_ylabel('Signal waveform')
axs[1,0].plot(t,ask_s);axs[1,0].set_xlabel('Time(s)');axs[1,0].set_ylabel('Signal waveform')
axs[0,1].psd(ak,len(ak),Fs);axs[0,1].set_title('Spectra of baseband signal and bandpass signal');axs[0,1].set_xlabel('frquency(Hz)')
axs[1,1].psd(ask_s,len(ask_s),Fs);axs[1,1].set_xlabel('frquency(Hz)')
fig1.tight_layout()
fig1.show()
# fig1.savefig(r'C:\Users\USER\Desktop\DSP_python\ASK signal modulation.png', dpi = 100)


psk_s_bb = upfirdn(h = [1]*L, x = 2*ak-1, up = L)
psk_s = psk_s_bb * np.sin(2*np.pi*fc*t/Fs)

# fig2, axs = plt.subplots(nrows = 2, ncols = 2)
# axs[0,0].plot(t,psk_s_bb);axs[0,0].set_title('Baseband and OOK waveforms');axs[0,0].set_xlabel('Time(s)');axs[0,0].set_ylabel('Signal waveform')
# axs[1,0].plot(t,psk_s);axs[1,0].set_xlabel('Time(s)');axs[1,0].set_ylabel('Signal waveform')
# axs[0,1].psd(ak,len(ak),Fs);axs[0,1].set_title('Spectra of baseband signal and bandpass signal');axs[0,1].set_xlabel('frquency(Hz)')
# axs[1,1].psd(psk_s,len(psk_s),Fs);axs[1,1].set_xlabel('frquency(Hz)')
# fig2.tight_layout()
# fig2.show()
# fig2.savefig(r'C:\Users\USER\Desktop\DSP_python\PSK signal modulation.png', dpi = 100)


fsk1_s_bb = upfirdn(h = [1]*L, x = ak, up = L)
fsk2_s_bb = upfirdn(h = [1]*L, x = -ak+1, up = L)

fsk1_s_f1 = fsk1_s_bb * np.sin(2*np.pi*fc*t/Fs)
fsk2_s_f2 = fsk2_s_bb * np.sin(2*np.pi*fm*t/Fs)
fsk_s = fsk1_s_f1 + fsk2_s_f2


# fig3, axs = plt.subplots(nrows = 2, ncols = 2)
# axs[0,0].plot(t,fsk1_s_bb);axs[0,0].set_title('Baseband and OOK waveforms');axs[0,0].set_xlabel('Time(s)');axs[0,0].set_ylabel('Signal waveform')
# axs[1,0].plot(t,fsk_s);axs[1,0].set_xlabel('Time(s)');axs[1,0].set_ylabel('Signal waveform')
# axs[0,1].psd(ak,len(ak),Fs);axs[0,1].set_title('Spectra of baseband signal and bandpass signal');axs[0,1].set_xlabel('frquency(Hz)')
# axs[1,1].psd(fsk_s,len(fsk_s),Fs);axs[1,1].set_xlabel('frquency(Hz)')
# fig3.tight_layout()
# fig3.show()
# fig3.savefig(r'C:\Users\USER\Desktop\DSP_python\FSK signal modulation.png', dpi = 100)

'''
ASK Demodulation with matched filter
'''
m_c = np.ones(L) # message signal one bit
s_c = np.sin(2*np.pi*fc*t/Fs)
r = s_c * ask_s
ASK_S = signal.fftconvolve(r,m_c)
ASK_S = ASK_S[L-1::L]       #sample at every sampling instant and detect
ASK_S = ASK_S/(np.max(ASK_S))   #normalization
ak_hat = (ASK_S > 0.7).astype(int)
print('AKS bit = ', ak_hat)

'''
ASK Demodulation with matched filter(Carrier phase error)
'''
P_error = 30 * (np.pi/180)
s_c_error = np.sin(2*np.pi*fc*t/Fs+P_error)
r_error = s_c_error * ask_s
ASK_S_error = signal.fftconvolve(r_error,m_c)

'''
ASK Demodulation with matched filter(Carrier frequency error)
'''
frequency_error = 40
s_c_f_error = np.sin(2*np.pi*(fc+frequency_error)*t/Fs)
r_f_error = s_c_f_error * ask_s
ASK_S_f_error = signal.fftconvolve(r_f_error,m_c)

z = hilbert(np.diff(r))
z_envelope = abs(z)


fig4, axs = plt.subplots(nrows = 2, ncols = 2)
axs[0,0].plot(ask_s_bb);axs[0,0].set_title('Information signal');axs[0,0].set_xlabel('Time(s)');axs[0,0].set_ylabel('Signal waveform')
axs[1,0].plot(ASK_S);axs[1,0].set_title('matched filter output');axs[1,0].set_xlabel('Time(s)');axs[1,0].set_ylabel('Signal waveform')
axs[0,1].plot(ask_s_bb);axs[0,1].set_title('Information signal');axs[0,1].set_xlabel('Time(s)');axs[0,1].set_ylabel('Signal waveform')
axs[1,1].plot(ASK_S_error);axs[1,1].set_title('matched filter output(Phsae error)');axs[1,1].set_xlabel('Time(s)');axs[1,1].set_ylabel('Signal waveform')
fig4.tight_layout()
fig4.show()
# fig4.savefig(r'C:\Users\USER\Desktop\DSP_python\ASK signal Demodulation(matched filter).png', dpi = 100)



fig5, axs = plt.subplots(nrows = 2, ncols = 2)
axs[0,0].plot(ask_s_bb);axs[0,0].set_title('Information signal');axs[0,0].set_xlabel('Time(s)');axs[0,0].set_ylabel('Signal waveform')
axs[1,0].plot(ASK_S_f_error );axs[1,0].set_title('matched filter output(frequency error)');axs[1,0].set_xlabel('Time(s)');axs[1,0].set_ylabel('Signal waveform')
axs[0,1].plot(ask_s_bb);axs[0,1].set_title('Information signal');axs[0,1].set_xlabel('Time(s)');axs[0,1].set_ylabel('Signal waveform')
axs[1,1].plot(z_envelope);axs[1,1].set_title('envelope detector output');axs[1,1].set_xlabel('Time(s)');axs[1,1].set_ylabel('Signal waveform')
fig5.tight_layout()
fig5.show()
# fig5.savefig(r'C:\Users\USER\Desktop\DSP_python\ASK signal Demodulation(Carrier error).png', dpi = 100)


'''
FSK Demodulation with matched filter(Coherent)
'''
y1 = np.sin(2*np.pi*fc*t/Fs) * fsk_s
y2 = np.sin(2*np.pi*fm*t/Fs) * fsk_s

FSK_y1 = signal.fftconvolve(y1,m_c)
FSK_y2 = signal.fftconvolve(y2,m_c)
FSK_y = FSK_y1 - FSK_y2

FSK_Y = FSK_y[L-1::L]       #sample at every sampling instant and detect
FSK_Y = FSK_Y/(np.max(FSK_Y))   #normalization
FSK_hat = (FSK_Y > 0.7).astype(int)

print('FSK BIt = ', FSK_hat)

'''
FSK Demodulation with matched filter(Noncoherent)
'''

z_FSK = hilbert(np.diff(fsk_s))
z_FSK = abs(z_FSK)


# fig6, axs = plt.subplots(nrows = 2, ncols = 2)
# axs[0,0].plot(psk_s_bb);axs[0,0].set_title('Information signal');axs[0,0].set_xlabel('Time(s)');axs[0,0].set_ylabel('Signal waveform')
# axs[1,0].plot(FSK_y);axs[1,0].set_title('matched filter output(frequency error)');axs[1,0].set_xlabel('Time(s)');axs[1,0].set_ylabel('Signal waveform')
# axs[0,1].plot(psk_s_bb);axs[0,1].set_title('Information signal');axs[0,1].set_xlabel('Time(s)');axs[0,1].set_ylabel('Signal waveform')
# axs[1,1].plot(z_FSK);axs[1,1].set_title('envelope detector output');axs[1,1].set_xlabel('Time(s)');axs[1,1].set_ylabel('Signal waveform')
# fig6.tight_layout()
# fig6.show()
# fig6.savefig(r'C:\Users\USER\Desktop\DSP_python\FSK signal Demodulation.png', dpi = 100)

#%%

