'''
Date : 2022.05.18
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
GPIO.output(Triger,True)
GPIO.output(reset,True)
GPIO.output(SHDN,False)
bus = 0
device = 0

spi = spidev.SpiDev()
spi.open(bus, device)
spi.max_speed_hz = 1000000
spi.mode = 0b00

buffer = [0x0000, 0x0e00, 0x0000, 0x0000, 0x4000, 0x4000, 0x4000, 0x4000, 0x0000, 0x1f00, 0x1f00, 0x1f00, 0x1f00, 0x0000, 0x0000, 0x0000, 0x000e, 0x0000, 0x0000, 0x0000, 0x0000, 0x3232, 0x3232, 0x0111, 0xffff, 0x0101, 0x0101, 0x0003, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x4000, 0x2000, 0x2000, 0x4000, 0x0001, 0x0200, 0x0a3d, 0x7100, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x07d0, 0x0000, 0x0000, 0x0100, 0x03e8, 0x0000, 0x0000, 0x0100, 0x0bb8, 0x0000, 0x0000, 0x0100, 0x0fa0, 0x0000, 0x0000, 0x0100, 0x0001, 0x0001]
reg_add = [0x0000, 0x0001, 0x0002, 0x0003, 0x0004, 0x0005, 0x0006, 0x0007, 0x0008, 0x0009, 0x000a, 0x000b, 0x000c, 0x000d, 0x000e, 0x001f, 0x0020, 0x0022, 0x0023, 0x0024, 0x0025, 0x0026, 0x0027, 0x0028, 0x0029, 0x002a, 0x002b, 0x002c, 0x002d, 0x002e, 0x002f, 0x0030, 0x0031, 0x0032, 0x0033, 0x0034, 0x0035, 0x0036, 0x0037, 0x003e, 0x003f, 0x0040, 0x0041, 0x0042, 0x0043, 0x0044, 0x0045, 0x0047, 0x0050, 0x0051, 0x0052, 0x0053, 0x0054, 0x0055, 0x0056, 0x0057, 0x0058, 0x0059, 0x005a, 0x005b, 0x005c, 0x005d, 0x005e, 0x005f, 0x001e, 0x001d]


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
        spi.close()
        print('end')
    def Setup_device(self):
        GPIO.output(reset,False)
        time.sleep(1e-5)
        GPIO.output(reset,True)
        GPIO.output(EN_CVDDX,True)       
    def Start_pattern(self):
        GPIO.output(Triger,False)
    def Stop_pattern(self):
        GPIO.output(Triger,True)

if __name__ == "__main__":
    print('START')
    P = PADVL(reg_add,buffer)
#     P.Setup_device()
    P.send_spi_data()
    P.Start_pattern()
#     for i in range(100):
#         P.Start_pattern()
#         time.sleep(1)
#         P.Stop_pattern()
#         time.sleep(1)

