'''
Date : 2022.05.20
Title: PADVL DDS chip Control
By: KJS
'''

import numpy as np
import spidev
import time
import RPi.GPIO as GPIO

EN_CVDDX = 17
Triger = 27
SHDN = 22
reset = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(EN_CVDDX, GPIO.OUT)
GPIO.setup(Triger, GPIO.OUT)
GPIO.setup(SHDN, GPIO.OUT)
GPIO.setup(reset, GPIO.OUT)

GPIO.output(EN_CVDDX,False)
# time.sleep(0.5)
GPIO.output(Triger,True)
# time.sleep(0.5)
GPIO.output(reset, True)
# time.sleep(0.5)
GPIO.output(SHDN,False)


bus = 0
device = 0

spi = spidev.SpiDev()
spi.open(bus, device)
spi.max_speed_hz = 1000000
spi.mode = 0b00

buffer = [0x0e00]
reg_add = [0x0001]

class PADVL:
    def __init__(self,reg_add, buffer):
        self.reg_add = reg_add
        self.buffer = buffer
        self.SUM_result = []
        self.Data_list = []
        
    def send_spi_data(self):        
        for i in range(len(self.buffer)):
            self.SUM_result.append(self.reg_add[i])
            self.SUM_result.append(self.buffer[i])
        for j in range(len(self.SUM_result)):
            MSB = (self.SUM_result[j]>>8) & 0xFF
            self.Data_list.append(MSB)
            LSB = self.SUM_result[j] & 0xFF
            self.Data_list.append(LSB)
        spi.xfer(self.Data_list)
        print('end')
    def Setup_device(self):
        GPIO.output(reset,False)
        time.sleep(0.05)
        GPIO.output(reset,True)
        time.sleep(0.05)
        GPIO.output(EN_CVDDX,True)
        time.sleep(0.05)
#         GPIO.output(SHDN,True)
    def Start_pattern(self):
        GPIO.output(Triger,False)
    def Stop_pattern(self):
        GPIO.output(Triger,True)

if __name__ == "__main__":
    print('START')

    P = PADVL(reg_add,buffer)
    P.Setup_device()
    P.send_spi_data()
#     P.Start_pattern()
    
    addr = reg_add[0]
    read_addr = 0x8000 + addr

    result1 = []

    MSB1 = (read_addr>>8) & 0xFF
    result1.append(MSB1)
    LSB1 = read_addr & 0xFF
    result1.append(LSB1)
    spi.xfer(result1)
    reg_data = spi.xfer([0,0])
    print(hex(reg_data[1]),hex(reg_data[0]))
    spi.close()
#     GPIO.cleanup()

