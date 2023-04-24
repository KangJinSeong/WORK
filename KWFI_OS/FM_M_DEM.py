#%%
'''
Date: 2021.08.26
Title: Frequency modulating and modulated signal(FM)
By: Kang Jin Seong
'''
from scipy.fftpack import fft, ifft, fftshift, ifftshift
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import chirp, hilbert
from scipy import signal

ts = 1/2000 # sampling interval[sec]
fs = 1/ts # sampling Frequency
fc = 300 # carrier frequency
kf = 50 # frequency sensitivity[Hz/volt]

'''
For Signal 1 : multilevel rectangular pulse sequence
'''

def mt_signal():
    y = []
    y1 = (np.ones((1,int(0.05*fs))).tolist())[0]
    y2 = ((np.ones((1,int(0.05*fs)))*-2).tolist())[0]
    y3 = (np.zeros((1,int(0.05*fs))).tolist())[0]
    y.extend(y1)
    y.extend(y2)
    y.extend(y3)
    return y

m = mt_signal()
m = np.array(m)

integ_m = (np.zeros((1,int(len(m)))).tolist())[0] #배열 만들때는 list[]
integ_m[0] = 0
for i in range(0,len(m)-1):
    integ_m[i+1] = integ_m[i] + m[i]*ts

integ_m = np.array(integ_m) #신호처리를 위한 계산을 할때에는 Array[] 변경

t = np.arange(start = 0, stop = 0.15, step = 1/fs) #time base
s_m = np.cos((2*np.pi*(fc*t+kf*integ_m)))

NFFT = len(t)
f = np.arange(start = -NFFT/2, stop = NFFT/2)*(fs/NFFT)
M = fftshift(fft(m,NFFT))/NFFT
S_M = fftshift(fft(s_m,NFFT))/NFFT

fig1, axs = plt.subplots(nrows = 2, ncols = 2)
axs[0,0].plot(t,m);axs[0,0].set_title('Message signal');axs[0,0].set_xlabel('Time(s)')
axs[1,0].plot(t,s_m);axs[1,0].set_title('Modulated signal');axs[1,0].set_xlabel('Time(s)')
axs[0,1].plot(f,abs(M));axs[0,1].set_title('Magnitude spectrum of the message signal');axs[0,1].set_xlabel('frquency(Hz)')
axs[1,1].plot(f,abs(S_M));axs[1,1].set_title('Magnitude spectrum of the modulated siganl');axs[1,1].set_xlabel('frquency(Hz)')
fig1.tight_layout()
fig1.show()

'''
For Signal 2 : triangular pulse with pulse width tau2 = 0.1 and amplitude = 2
'''
def triangle_signal():
    y = []
    y1 = list(signal.triang((0.1*fs)))
    y2 = (np.zeros((1,int(0.05*fs))).tolist())[0]
    y.extend(y2)
    y.extend(y1)
    y.extend(y2)
    return y

m1 = triangle_signal()
m1 = np.array(m1)

integ_m1 = (np.zeros((1,int(len(m1)))).tolist())[0] #배열 만들때는 list[]
integ_m1[0] = 0
for i in range(0,len(m)-1):
    integ_m1[i+1] = integ_m1[i] + m1[i]*ts

integ_m1 = np.array(integ_m1) #신호처리를 위한 계산을 할때에는 Array[] 변경

t1 = np.arange(start = -0.1, stop = 0.1, step = 1/fs) #time base
s_m1 = np.cos((2*np.pi*(fc*t1+kf*integ_m1)))

NFFT = len(t1)
f1 = np.arange(start = -NFFT/2, stop = NFFT/2)*(fs/NFFT)
M1 = fftshift(fft(m1,NFFT))/NFFT
S_M1 = fftshift(fft(s_m1,NFFT))/NFFT

fig2, axs = plt.subplots(nrows = 2, ncols = 2)
axs[0,0].plot(t1,m1);axs[0,0].set_title('Message signal');axs[0,0].set_xlabel('Time(s)')
axs[1,0].plot(t1,s_m1);axs[1,0].set_title('Modulated signal');axs[1,0].set_xlabel('Time(s)')
axs[0,1].plot(f1,abs(M1));axs[0,1].set_title('Magnitude spectrum of the message signal');axs[0,1].set_xlabel('frquency(Hz)')
axs[1,1].plot(f1,abs(S_M1));axs[1,1].set_title('Magnitude spectrum of the modulated siganl');axs[1,1].set_xlabel('frquency(Hz)')
fig2.tight_layout()
fig2.show()
# plt.show()

'''
Noise Channel

'''
snr_dB = 30             #SNR in dB
snr = pow(10,snr_dB/10)    #linear SNR
signal_power = pow(np.linalg.norm(s_m),2)/len(t)  #modulated signal power(신호벡터크기 계산)
signal_power1 = pow(np.linalg.norm(s_m1),2)/len(t1)    #modulated signal power(신호벡터크기 계산)
noise_power = signal_power/snr  #noise power
noise_power1 = signal_power1/snr  #noise power
noise_std = np.sqrt(noise_power)    #noise standard deviation
noise_std1 = np.sqrt(noise_power1)    #noise standard deviation
noise = noise_std*np.random.normal(size = (len(t))) # awgn noise
noise1 = noise_std1*np.random.normal(size = (len(t1))) # awgn noise
r = noise + s_m # add noise to the modulated signal
r1 = noise1 + s_m1 # add noise to the modulated signal
'''
Coherent demodulation
'''
z = hilbert(r) # form the analytical signal from the received freq/phase perfectly
z1= hilbert(r1)
inst_phase = np.unwrap(np.angle(z)) # instaneous phase
inst_phase1 = np.unwrap(np.angle(z1)) # instaneous phase

demod = (1/(2*np.pi*kf))*(np.diff(inst_phase)/ts)  #Differentiate and scale phase
demod1 = (1/(2*np.pi*kf))*(np.diff(inst_phase1)/ts)  #Differentiate and scale phase
fig3, axs = plt.subplots(nrows = 2, ncols = 2)
axs[0,0].plot(t,m);axs[0,0].set_title('Message signal');axs[0,0].set_xlabel('Time(s)')
axs[1,0].plot(t[0:len(t)-1],demod);axs[1,0].set_title('Modulated signal');axs[1,0].set_xlabel('Time(s)')
axs[0,1].plot(t1,m1);axs[0,1].set_title('Message signal');axs[0,1].set_xlabel('Time(s)')
axs[1,1].plot(t1[0:len(t1)-1],demod1);axs[1,1].set_title('Modulated signal');axs[1,1].set_xlabel('Time(s)')
# axs[1,0].set_ylim([-2, 2]); axs[1,1].set_ylim([0, 2])
fig3.tight_layout()
fig3.show()

# fig3.savefig(r'C:\Users\USER\Desktop\DSP_python\Coherent demodulation Signal(FM).png')




'''
Noncoherent demodulation
'''

z = hilbert(np.diff(r)) # form the analytical signal from the received freq/phase perfectly
z1= hilbert(np.diff(r1))
inst_amplitude = abs(z)
inst_amplitude1 = abs(z1)

fig4, axs = plt.subplots(nrows = 2, ncols = 2)
axs[0,0].plot(t,m);axs[0,0].set_title('Message signal');axs[0,0].set_xlabel('Time(s)')
axs[1,0].plot(t[0:len(t)-1],inst_amplitude);axs[1,0].set_title('Modulated signal');axs[1,0].set_xlabel('Time(s)')
axs[0,1].plot(t1,m1);axs[0,1].set_title('Message signal');axs[0,1].set_xlabel('Time(s)')
axs[1,1].plot(t1[0:len(t1)-1],inst_amplitude1);axs[1,1].set_title('Modulated signal');axs[1,1].set_xlabel('Time(s)')
# axs[1,0].set_ylim([-2, 2]); axs[1,1].set_ylim([0, 2])
fig4.tight_layout()
fig4.show()
# fig4.savefig(r'C:\Users\USER\Desktop\DSP_python\Noncoherent demodulation Signal(FM).png')

plt.show()

# %%