"""
Rx Signal Porcessing for CSS Underwater Comm.
Version : Test
Writer : Kibae Lee (Kyungwon Industry)
2020.09.14
"""

""" Import mudules """
print("Import mudules....")

import pyaudio # Audio device interface library
import numpy as np # Numerical computing library
import pandas as pd # Data frame managing libary
import warnings # Warning message library
import time # Computing time measurement [debug]

# Signal processing library
from scipy.signal import chirp, decimate, hilbert, find_peaks
from scipy.fftpack import fft, ifft

from multiprocessing import Queue, Process # Multiprocessing library
from matplotlib import pyplot as plt # Plotting data [debug]

warnings.filterwarnings("ignore") # Ingore warning message

""" Initialize """
print("Initialize.....")

# ========== Data read ========== #
# Audio device setup
Fs = 192000 # Sampling frequency
dt = 1/Fs # Sampling time
NumFrame = 19200 # Number of samples
record_time = 120 # Record time

p = pyaudio.PyAudio()
stream = p.open(format = pyaudio.paInt16, channels = 1, rate = Fs, input = True, frames_per_buffer = NumFrame)

# User ID
User_ID = [0, 1, 1, 1, 0, 0, 1, 0]

# ========== Pre-processing ========== #
# Carrier for pre-processing
f_carr = 30000 # Carrier frequency (Hz)
t_carr = np.arange(0,(NumFrame)/Fs, dt) # Frame
sig_carr = np.cos(2*np.pi*f_carr*t_carr) # Carrier signal
rate_deci = 12 # Decimate rate

# ========== Signal processing ========== #
# Filter Coefficient
Fs_deci = Fs/rate_deci # Decimated sampling frequency
dt_deci = 1/Fs_deci # Decimated sampling time
NumFrame_deci =  NumFrame/rate_deci # Decimated number of samples
t0_deci = np.arange(0,0.128,dt_deci) # Frame of source signal
Coeff_0 = chirp(t0_deci, f0 = 4000, f1 = 0, t1 = 0.128, method = 'linear') # Coefficient for bit 0
Coeff_1 = chirp(t0_deci, f0 = 0, f1 = 4000, t1 = 0.128, method = 'linear') # Coefficient for bit 1

L1 = int(NumFrame_deci) * 2 # data length
M1 = len(Coeff_0) # filter length
N1 = L1 + M1 - 1 # Block length

# FFT Coefficient
H1_0 = fft(Coeff_0, N1) # For bit 0
H1_1 = fft(Coeff_1, N1) # For bit 1

# ========== Post processing ========== #
alpha = 10 # Threshold bias value
Dist = round(M1 * 0.95) # Distance (peak to peak)

# ========== Queue ========== #
ADC_Q = Queue()
Pre_Proc_Q0 = Queue()
Pre_Proc_Q1 = Queue()
Sig_Proc_Q0 = Queue()
Sig_Proc_Q1 = Queue()

""" Processing """
# Process0 : ADC data read
def ADC():
    for i in range(0, int(Fs/NumFrame * record_time)):
        ADC_data = np.fromstring(stream.read(NumFrame), np.int16)/10000
        ADC_Q.put(ADC_data) # Put Queue

# Process1 : Pre-Processing
def Pre_Process():
    for i in range(0, int(Fs/NumFrame * record_time)):
        ADC_data = ADC_Q.get() # Get Queue
        Sig_mul = ADC_data * sig_carr # Multiply Carrier
        
        y0 = decimate(Sig_mul, rate_deci) # Decimation (Low Pass Filter)
        
        # Put Queue
        Pre_Proc_Q0.put(y0)
        Pre_Proc_Q1.put(y0)

def Sig_Process0():
    X1 = [0 for x in range(M1-1)]
    for i in range(0, int((Fs_deci/NumFrame_deci * record_time)/2)):
        y0 = []
        for k in range(2):
            Y0 = Pre_Proc_Q0.get() # Queue get
            y0.extend(Y0)
        X1.extend(y0) # Overlap add
        
        # Cross-correlation
        Y1 = ifft(fft(X1)*H1_0)
        y1 = Y1[M1-1:N1].real

        # Envelope
        H = hilbert(y1).real + hilbert(-y1).real
        r = np.power(np.sqrt(np.power(y1,2) + np.power(H,2)),2)
        
        Sig_Proc_Q0.put(r) # Queue put
        
        X1 = X1[L1:N1] # Overlap save
    
def Sig_Process1():
    X1 = [0 for x in range(M1-1)]
    for i in range(0, int((Fs_deci/NumFrame_deci * record_time)/2)):
        y0 = []
        for k in range(2):
            Y0 = Pre_Proc_Q1.get() # Queue get
            y0.extend(Y0)
        X1.extend(y0) # Overlap add
        
        # Cross-correlation
        Y1 = ifft(fft(X1)*H1_1)
        y1 = Y1[M1-1:N1].real

        # Envelope
        H = hilbert(y1).real + hilbert(-y1).real
        r = np.power(np.sqrt(np.power(y1,2) + np.power(H,2)),2)
        
        Sig_Proc_Q1.put(r) # Queue put

        X1 = X1[L1:N1] # Overlap save
        
def Post_Process():
    #results = []
    code = [-1 for x in range(8)] # SOF 2bit, ID 4bit, EOF 2bit
    for i in range(0, int((Fs_deci/NumFrame_deci * record_time)/2)):
        # Queue get
        r0 = Sig_Proc_Q0.get() # Queue get
        r1 = Sig_Proc_Q1.get() # Queue get
        
        y = r0-r1 # 2D vector convert to 1D vector with whitening
        
        # Threshold estimation with moving average
        yt0 = pd.Series(y)
        yt1 = yt0.rolling(160).mean()
        yt2 = yt1.tolist()
        yt3 = yt1[159:]
        yt_p = max(yt3) + (max(yt3) - min(yt3)) + alpha
        yt_n = min(yt3) - (max(yt3) - min(yt3)) - alpha

        # Peak & Valley detection
        Peak_ind0, _ = find_peaks(y, height = yt_p, distance = Dist)        
        Peak_ind1, _ = find_peaks(-y, height = -yt_n, distance = Dist)
        
        # Code identification
        L_ind0 = len(Peak_ind0)
        L_ind1 = len(Peak_ind1)
        L_sum = L_ind0 + L_ind1
        
        if L_sum == 0 :
            data = []
        elif L_sum == 1 :
            if L_ind0 > L_ind1 :
                data = 0
            else :
                data = 1
            code.pop(0)
            code.append(data)
        elif L_ind0 + L_ind1 == 2 :
            if L_ind0 == 0 :
                data = [1, 1]
            elif L_ind1 == 0 :
                data = [0, 0]
            else :
                if Peak_ind0 < Peak_ind1 :
                    data = [0, 1]
                else :
                    data = [1, 0]
            code.pop(0)
            code.pop(0)
            code.extend(data)
            
        if L_sum > 0 :
            if np.array_equal(code, User_ID) == True :
                print("User detect!!! / ID : ", User_ID)
                
        #results.extend(y)
    
    #plt.plot(results)
    #plt.show()
    
""" Main """    
# Define process
process0 = Process(target = ADC)
process1 = Process(target = Pre_Process)
process2 = Process(target = Sig_Process0)
process3 = Process(target = Sig_Process1)
process4 = Process(target = Post_Process) # Threading

# Start Process
print("Start process.....")
process0.start()
process1.start()
process2.start()
process3.start()
process4.start()

ts = time.time() # start time

# Process close
process0.join()
process1.join()
process2.join()
process3.join()
process4.join()

# Queue close
ADC_Q.close()
Pre_Proc_Q0.close()
Pre_Proc_Q1.close()
Sig_Proc_Q0.close()
Sig_Proc_Q1.close()

print("Computing time : ", time.time() - ts) # computing time

# ADC device close
stream.stop_stream()
stream.close()
p.terminate()