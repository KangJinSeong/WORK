import L76X
import time
import math
import config
import serial
Temp = '0123456789ABCDEF*'

ser= serial.Serial("/dev/ttyS0",9600)

# try:
x=L76X.L76X()
a = config.config()
x.L76X_Set_Baudrate(9600)
data = x.SET_NMEA_BAUDRATE_115200

Check = ord(data[1])


for i in range(2, len(data)):
	Check = Check ^ ord(data[i]) 

# ~ print(Check)

data = data + Temp[16]
# ~ print(data)
data = data + Temp[int((Check/16))]
# ~ print(data)
data = data + Temp[(Check%16)]
print(data)
a = data.encode()
print(a)
ser.write(a) 
# ~ x.L76X_Send_Command(x.SET_NMEA_BAUDRATE_115200)
