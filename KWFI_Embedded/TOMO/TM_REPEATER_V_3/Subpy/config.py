'''
Date: 2023.03.28
Title: Waveshare L76X GPS HAT Function python
By: Kang Jin seong
'''
import serial
import RPi.GPIO as GPIO

Temp = '0123456789ABCDEF*'

class config(object):
    FORCE  = 17
    STANDBY= 4
    def __init__(ser, Baudrate = 9600):
        ser.serial = serial.Serial("/dev/ttyS0",Baudrate)
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(ser.FORCE, GPIO.IN)
        GPIO.setup(ser.STANDBY, GPIO.OUT)
        GPIO.output(ser.STANDBY, GPIO.HIGH)

    def Uart_SendByte(ser, value): 
        ser.serial.write(value) 

    def Uart_SendString(ser, value): 
        ser.serial.write(value)

    def Uart_ReceiveByte(ser): 
        return ser.serial.read(1)

    def Uart_ReceiveString(ser, value): 
        data = ser.serial.read(value)
        return data

    def Uart_Set_Baudrate(ser, Baudrate):
        ser.serial = serial.Serial("/dev/ttyS0",Baudrate)

    def close(ser):
        GPIO.cleanup()
        ser.serial.close()

