import pyaudio # Audio device interface library
import numpy as np # Numerical computing library
import time

p = pyaudio.PyAudio()

volume = 0.5     # range [0.0, 1.0]
fs = 192000       # sampling rate, Hz, must be integer
numframe = 19200
f = 10000        # sine frequency, Hz, may be float
t = np.arange(start = 0, stop = numframe)
# generate samples, note conversion to float32 array
samples = (np.sin(2*np.pi*(f/fs)*t)).astype(np.float32).tobytes()

# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)
time.sleep(1)
# play. May repeat with different volume values (if done interactively) 
stream.write(samples)

stream.stop_stream()
stream.close()

p.terminate()