#%%
'''
Date: 2021.09.28
Title: signal BER(bit error rate)
By: Kang Jin Seong
'''
from scipy.fftpack import fft, ifft, fftshift, ifftshift
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import chirp, hilbert
from scipy import signal
from numpy import sum, isrealobj,sqrt
from numpy.random import standard_normal
from scipy.signal import upfirdn
from scipy.special import erfc  #Complementary error function


def awgn(s,SNRdB,L=1):
    '''
    AWGN channel

    add AWGN noise to input signal the function adds AWGN noise vector to signal
    's' to generate a resulting signal vector 'r' of specified SNR in dB it also
    returns the noise vector 'n' that is added to the signal 's' and the power
    spectral density No of noise added

    Parameters:
     s : input/transmitted signal vector
     SNRdB: desired signal to noise ratio (expressed in dB)
            for the received signal
     L : oversampling factor (applicable for waveform simulation)
         default L = 1

    returns:
      r: received signal vector ( r = s + n)
    '''
    
    gamma = 10**(SNRdB/10)  #SNR to linear scale      # Eb/No = 10^(x/10)
    if s.ndim == 1: # if s is single dimensional vector
        P = L * sum(abs(s)**2)/len(s) # Actual power in the vector # ex: pow(np.linalg.norm(s_m),2)/len(t)
    else:   # multi-dimensional signals like MFSK
        P = L*sum(sum(abs(s)**2))/len(s)    #if s is a matrix[M x N]
    N0 = P/gamma # Find the noise spectral density

    if isrealobj(s):    # check if input is real/complex object type
        n = sqrt(N0/2)*standard_normal(s.shape) #computed noise
    else:
        n = sqrt(N0/2)*standard_normal(s.shape)+1j*standard_normal(s.shape)
    
    r = s + n   #received signal

    return r

def bpsk_mod(ak, L):
    '''
    Function to modulate an incoming binary stream using BPSK(baseband)
    
    Parameters:
     ak : input binary data stream (0's and 1's) to modulate
      L : oversampling factor(Tb/Ts)
    
    Returns:
        (s_bb,t): tuple of following variables
            s_bb : BPSK modulated signal(baseband) = s_bb(t)
            t : generated time base for the modulated signal
    '''
    s_bb = upfirdn(h = [1]*L, x = 2*ak-1, up = L)   # NRZ encoder
    t = np.arange(start = 0, stop = len(ak)*L)  #discrete time base
    return(s_bb, t)

def bpsk_dmod(r_bb,L):
    '''
    Function to demodulate a BPSK (baseband) signal
    Parameters:
        r_bb : received signal at the receiver front end(baseband)
        L : oversmapling factor(Tsym/Ts)
    
    Returns:
        ak_hat : detected / estimated bianry stream
    '''
    x = np.real(r_bb)   # I arm
    x = np.convolve(x, np.ones(L))  #integrate for Tb duration (L samples)
    x = x[L-1:-1:L] # I arm = sample at every L
    ak_hat = (x > 0).transpose()    # threshold detector
    return ak_hat

N = 100000  #number of symbols to transmit
EbN0dB = np.arange(start = -4, stop = 11, step = 2) #Eb/N0 range in dB for simulation   
L = 16  # oversmapling factor, L = Tb/Ts ( Tb = bit period, Ts = sampling period)

# if a carrier is used, use L = fs/Fc, where Fs >> 2*Fc
Fc = 800 # carrier frequency
Fs = L*Fc   #sampling frequency
BER = np.zeros(len(EbN0dB)) # for BER values for each Eb/N0
ak = np.random.randint(2, size = N) # uniform random symbols from 0's and 1's

(s_bb, t) = bpsk_mod(ak,L) # BPSK modulation(waveform) - baseband

s = s_bb * np.sin(2*np.pi*Fc*t/Fs)  # with carrier
#waveforms at the transmitter

fig1, axs = plt.subplots(2,2)
axs[0,0].plot(t,s_bb)   #baseband wfm zoomed to first 10 bits
axs[0,0].set_xlabel('t(s)');axs[0,0].set_ylabel(r'$s_[bb](t)$-baseband')
axs[0,1].plot(t,s)  #transmitted wfm zoomed to first 10 bits
axs[0,1].set_xlabel('t(s)');axs[0,1].set_ylabel('s(t)-with carrier')
axs[0,0].set_xlim(0,10*L);axs[0,1].set_xlim(0,10*L)

#signal constellation at transmitter

axs[1,0].plot(np.real(s_bb), np.imag(s_bb), 'o')
axs[1,0].set_xlim(-1.5, 1.5);axs[1,0].set_ylim(-1.5, 1.5)

for i, EbN0 in enumerate(EbN0dB):   #enumerate: 반복문 사용 시 몇 번쨰 반복문인지 확인이 필요할 떄 사용 -> 튜플형태로 반환된다.
    # Compute and add AWGN Noise
    r = awgn(s,EbN0,L)   # refer Chapter sectuon 4.1
    r_bb = r* np.cos(2*np.pi*Fc*t/Fs)   # recovered baseband signal
    ak_hat = bpsk_dmod(r_bb, L)    # baseband correlation demodulator
    BER[i] = np.sum( ak != ak_hat)/N    # bit Error Rate Computation

    # Received signal waveform zoomed to first 10 bits
    axs[1,1].plot(t,r)  #received signal(with noise)
    axs[1,1].set_xlabel('t(s)'); axs[1,1].set_ylabel('r(t)')
    axs[1,1].set_xlim(0,10*L)
# Theoretical Bit/Symbol Error Rates
theoreticalBER = 0.5*erfc(np.sqrt(10**(EbN0dB/10))) # Theoretical bit error rate
# plots
fig2, ax1 = plt.subplots(nrows = 1, ncols = 1)
ax1.semilogy(EbN0dB, BER, 'k*', label = 'Simulated')    #Simulated BER
ax1.semilogy(EbN0dB, theoreticalBER, 'r-', label = 'Theoretical')
ax1.set_xlabel(r'$E_b/N_0$(dB)')
ax1.set_ylabel(r'Probability of Bit Error - $P_b$')
ax1.set_title(['Probability of Bit Error for BPSK modulation'])
ax1.legend()

# %%
