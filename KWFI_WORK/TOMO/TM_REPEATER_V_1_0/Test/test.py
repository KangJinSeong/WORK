import RPi.GPIO as GPIO
# import serial

# serialIP = serial.Serial('/dev/ttyS0', baudrate= 9600)

# serialIP.readline()

# import socket
# import time

# while True:
#     ipaddress = socket.gethostbyname(socket.gethostname())
#     if ipaddress == '127.0.0.1':
#         print('NOT')
#     else:
#         print(' ON ' + ipaddress)
#     time.sleep(1)

import os
import time
hostname = 'www.google.com'

response = os.system("ping -c 1 " + hostname)

if response == 0:
    print("Network active")
else:
    print("Network error")
