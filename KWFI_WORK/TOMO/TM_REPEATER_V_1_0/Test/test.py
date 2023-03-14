import RPi.GPIO as GPIO
import serial

serialIP = serial.Serial('/dev/ttyS0', baudrate= 9600)

# serialIP.readline()