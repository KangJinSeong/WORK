import serial
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import chirp

fs = 100000
fc = 1000
t = np.arange(start = 0, stop = 0.005, step = 1/fs)
y = np.cos(2*np.pi*fc*t)
g = chirp(t, f0 = 10, t1 = 0.005, f1 = 2000, method = 'linear')

# plt.figure()
# plt.plot(t,g)
# plt.show()
print(len(t))
print(len(y))
ser = serial.Serial('/dev/ttyUSB0',230400)

i = 0
while True:
    ser.write(str(g[i]).encode('ascii'))
    ser.write('\n'.encode('ascii'))
    print('{}'.format(g[i]))
#     sleep(0.2)
    i+=1
    if i == len(g):
        i = 0
#     for i in range(0,len(g)):
#         ser.write(str(g[i]).encode())
#         sleep(0.2)

        
