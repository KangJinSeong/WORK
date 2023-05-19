import RPi.GPIO as GPIO
import time
import datetime as dt
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.IN)

def my_callback(channel):
	dt1 = dt.datetime(year = a.year, month = a.month, day = a.day, hour = a.hour, minute = a.minute, second = a.second, microsecond = 0)
	print('1PPS time:', dt1)

GPIO.add_event_detect(23, GPIO.RISING, callback = my_callback)


p = dt.datetime.now().second

while True:
	x = dt.datetime.now().second
	if p != x:
		a = dt.datetime.now()
		print('Rasp time:',a)
	p = x
	
	
