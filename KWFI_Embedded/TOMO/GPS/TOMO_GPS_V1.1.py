
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
import struct
import socket



# ~ server_ip = '30.0.1.59'
# ~ s = socket.create_connection((server_ip, 2500))

# try:
x=L76X.L76X()
x.L76X_Set_Baudrate(9600)
x.L76X_Send_Command(x.SET_NMEA_BAUDRATE_115200)
time.sleep(2)
x.L76X_Set_Baudrate(115200)

# ~ x.L76X_Send_Command(x.SET_POS_FIX_400MS);

# ~ #Set output message
# ~ x.L76X_Send_Command(x.SET_NMEA_OUTPUT);


# ~ x.L76X_Exit_BackupMode();


GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.IN)
an = dt.datetime.now()
log_lat = "{:.4f}".format(0)
log_lon = "{:.4f}".format(0)


p = dt.datetime.now().second

def my_callback(channel):
	global state
	state = 1
	dt1 = dt.datetime(year = an.year, month = an.month, day = an.day, hour = an.hour, minute = an.minute, second = an.second, microsecond = 0)
	if state != 0:
		smsg ='&'+','+ str(dt1)+',' + log_lat+',' + log_lon +','+'%'
		# ~ s.sendall(smsg.encode())
		print('1PPS time:', dt1)

GPIO.add_event_detect(23, GPIO.RISING, callback = my_callback)

global state
state = 0

while True:
	
	if GPIO.input(23):
		pass
	else:
		state = 0
	
	Q = dt.datetime.now().second

	if p != Q:
		an = dt.datetime.now()
	
		if state == 0:
			smsg ='&'+','+ str(an)+',' + log_lat+',' + log_lon +'%'
			# ~ s.sendall(smsg.encode())
			print('Rasp time:',an)
	p = Q
	
	
	
	if state != 0:
		data = x.L76X_Gat_GNRMC()
		a = data.decode('utf-8')
		b = a.split('\r\n')
		# ~ print(b)
		for i in range(len(b)):
			c = b[i]
			d = c.split(',')
			if d[0] == '$GNRMC':
				if len(d) == 13 and len(d[3]) > 0:
					lat = d[3]
					lon = d[5]

					log_lat_dd = float(lat[0:2])
					log_lat_mm = float(lat[2:])/60
					log_lat = "{:.4f}".format(log_lat_dd + log_lat_mm)
					log_lon_dd = float(lon[0:3])
					log_lon_mm = float(lon[3:])/60
					log_lon = "{:.4f}".format(log_lon_dd + log_lon_mm)
					print("Lat :{}, Lon: {}".format(log_lat, log_lon))

				else:

					log_lat = "{:.4f}".format(0)
					log_lon = "{:.4f}".format(0)
		
