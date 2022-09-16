'''
Date: 2022.06.22
Title: 로라망 1차 시험 관련 코드 구현
By: Kang Jin Seong
'''

import serial
import time
import numpy as np
from scipy.signal import chirp, hilbert
import matplotlib.pyplot as plt
from scipy import signal
import struct


t = np.arange(start = 0, stop = 0.11, step = 1/fs) #Chirp time base
g1 = chirp(t, f0= 10, t1 = 0.11, f1 = 100, method = 'linear') # UP-chirpping signal(coefficient for bit 1)
y1_ch1 = signal.correlate(g1,g1, method= 'fft')     # using FFT cross-correlation
buf = struct.pack(">%sf" % len(y1_ch1), *y1_ch1)

# 시리얼 포트 초기화
ser = serial.Serial('/dev/ttyUSB0', baudrate = 9600, timeout = 1)

if ser.isOpen() == False:	#포트가 열려있지 않으면 오픈한다.
	ser.open()
	print("Now a serial port is open")
	

while True:

	if ser.readable():	#수신데이터가 있으면
		r_msg = ser.readline()
		print("Receiving messag:", r_msg)
	if r_msg.decode() == '':
		ser.write('NOT message'.encode('utf-8'))
		print(' NOT Message')
		time.sleep(3)
	if r_msg.decode() == '<<<<ON':
		msg = str(buf).encode('utf-8')
		print("COMPLITE")
		ser.write(msg)
		time.sleep(3)
		
ser.close()
