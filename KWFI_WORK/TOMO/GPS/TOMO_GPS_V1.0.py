
'''
Date: 2022.07.20
Title: 3차원해수유동 GPS 및 시간 데이터 전송
By: Kang Jin seong
'''


import L76X
import time
import math
import RPi.GPIO as GPIO
import datetime as dt
import serial
# ~ import struct
from socket import *
from select import *
from multiprocessing import Process

def GPS_Detect():	# 서브 프로세스로 실행할 함수
	x=L76X.L76X()
	x.L76X_Set_Baudrate(9600)
	x.L76X_Send_Command(x.SET_NMEA_BAUDRATE_115200)
	time.sleep(2)
	x.L76X_Set_Baudrate(115200)
	
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(23,GPIO.IN)
	an = dt.datetime.now()
	log_lat = "{:.4f}".format(0)
	log_lon = "{:.4f}".format(0)
	def my_callback(channel):
		dt1 = dt.datetime(year = an.year, month = an.month, day = an.day, hour = an.hour, minute = an.minute, second = an.second, microsecond = 0)
		print('1PPS time:', dt1)
		print("Lat :{}, Lon: {}".format(log_lat, log_lon))

	GPIO.add_event_detect(23, GPIO.RISING, callback = my_callback)

	p = dt.datetime.now().second

	while True:
		Q = dt.datetime.now().second
		if p != Q:
			an = dt.datetime.now()
			print('Rasp time:',an)
		p = Q
		
		data = x.L76X_Gat_GNRMC()
		a = data.decode('utf-8')
		b = a.split('\r\n')
		for i in range(len(b)):
			c = b[i]
			d = c.split(',')	
			if d[0] == '$GNRMC':
				if len(d) == 13 and len(d[3]) > 0:
					lat = d[3]
					lon = d[5]
					# ~ print(d)
					log_lat_dd = float(lat[0:2])
					log_lat_mm = float(lat[2:])/60
					log_lat = "{:.4f}".format(log_lat_dd + log_lat_mm)
					log_lon_dd = float(lon[0:3])
					log_lon_mm = float(lon[3:])/60
					log_lon = "{:.4f}".format(log_lon_dd + log_lon_mm)
					# ~ print("Lat :{}, Lon: {}".format(log_lat, log_lon))
				else:
					print('GPS Undectected')
					# ~ print(d)
					log_lat = "{:.4f}".format(0)
					log_lon = "{:.4f}".format(0)
					
if __name__ == '__main__':
	p = Process(target = GPS_Detect, args = () )
	p.start()
