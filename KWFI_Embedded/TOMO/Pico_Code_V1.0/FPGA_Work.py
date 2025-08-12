from machine import Pin
import utime

class FPGA_:
    def __init__(self):
        self.pin = 0
        
    def FPGA_Check(self,Working_set=Pin(9,mode=Pin.IN)):
        self.pin = Working_set
        try:
            if self.pin.value() == 0:
#                 print('Close')
                return 0
            else:
#                 print('Open')
                return 1
        except Exception as e:
            print('Error')
            return 2
        utime.sleep(0.1)

if __name__=='__main__':
    print(FPGA_().FPGA_Check())
