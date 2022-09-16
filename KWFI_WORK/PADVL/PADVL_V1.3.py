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

buffer = [0x0e00, 0x4000, 0x4000, 0x4000, 0x4000, 0x1f00, 0x1f00, 0x1f00, 0x1f00,0x000e, 0x3232, 0x3232, 0x0111, 0xffff, 0x0101, 0x0101, 0x0003, 0x4000, 0x2000, 0x2000, 0x4000, 0x0001, 0x2000, 0x0a3d, 0x7100,  0x07D0, 0x0100, 0x03e8,  0x0100, 0x0bb8,  0x0100, 0x0fa0, 0x0100, 0x0004]
reg_add = [0x0001, 0x0004, 0x0005, 0x0006, 0x0007, 0x0009, 0x000a, 0x000b,0x000c,0x0020, 0x0026, 0x0027, 0x0028, 0x0029, 0x002a, 0x002b, 0x002c, 0x0032, 0x0033, 0x0034, 0x0035, 0x0036, 0x0037, 0x003e, 0x003f,  0x0050, 0x0053, 0x0054,  0x0057, 0x0058,  0x005b, 0x005c, 0x005f,0x0060]


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
    
    addr = reg_add[1]
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
