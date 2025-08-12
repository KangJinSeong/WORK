from machine import UART, Pin
import time

class Uart_CONN:
    def __init__(self):
        self.tx1 = 0
        self.TRX_CON = 0
        self.rx1 = 0
        self.baud = 0
        
    def RS485READ(self,tx1=Pin(0),TRX_CON=Pin(22,mode=Pin.OUT),rx1=Pin(1),baud=115200):
        self.tx1 = tx1
        self.TRX_CON = TRX_CON
        self.TRX_CON.value(0)
        self.rx1 = rx1
        self.baud = baud
        self.uart1 = UART(0, baudrate=self.baud, tx=self.tx1, rx=self.rx1,timeout=5)
        self.uart1.init(self.baud,bits=8,parity=None,stop=1)
        while True:
            try:
                if self.uart1.any():
                    print('end')
                    Data = self.uart1.read().decode().split('\r')
                    T,D = Data[0][Data[0].index('=')+1:],Data[1][Data[1].index('=')+1:]  
                    time.sleep(0.1)
                    break
            except:
                print('end')
                T,D = 0,0
                break
        return T,D
    
    def RS232WRITE(self,DSPEN=0,TRXEN=0,TRXCSEN=0,DC12VMNT=0,MNTIN=0,BDTEMP=0,ENVTEMP=0,DEPTH=0,FPGAWORKING=0):
        self.tx1 = Pin(4)
        self.rx1 = Pin(5)
        self.baud = 9600
        #A = Pin(2,mode=Pin.OUT)
        #A.value(1)
        self.uart2 = UART(1, baudrate=self.baud, tx=self.tx1, rx=self.rx1)
        self.uart2.init(self.baud,bits=8,parity=None,stop=1)
        
        RSDAT = '%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(DSPEN,TRXEN,TRXCSEN,DC12VMNT,MNTIN,BDTEMP,ENVTEMP,DEPTH,FPGAWORKING)
        
        self.uart2.write(RSDAT)
        
        return 0

if __name__ == '__main__':
    print(Uart_CONN().RS485READ())
    print(Uart_CONN().RS232WRITE())



