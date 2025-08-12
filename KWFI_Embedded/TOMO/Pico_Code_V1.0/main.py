# from BoardTemp import Board_temp as Bt
# from FPGA_Work import FPGA_
# from UART import Uart_CONN as Conn
# from ADC import MUX
# import time
# 
# err_check = 0#error 체크 함수
# while True:
#     DSPEN,TRXPSEN,TRXCSEN,DC12VMNT,MNTIN,err_check = MUX().MUX_CHECK(outputV=0,limit=12,Err_check=err_check)#DSPEN,TRXPSEN,TRXCSEN,DC12VMNT,MNTIN,err_check 반환
#     err_check = err_check#만약 해당 함수가 1로 바뀌게 되면 전역 변수에 의해 다음 반복문 시 ADC 함수에 1이 들어가게 된다.
#     BoardTemp = Bt().read_temp() # 0 : error Data , 보드 온도 반환
#     Working_check = FPGA_().FPGA_Check() # 0 : close , 1 : open, 2 : error, FPGA 데이터 반환 현재 사용 X
#     ENVTEMP,Depth = Conn().RS485READ() # 0 : error Data, UART통신을 통해 받은 센서 온도 및 깊이 데이터 반환
# 
#     Conn().RS232WRITE(DSPEN=DSPEN,TRXEN=TRXPSEN,TRXCSEN=TRXCSEN,DC12VMNT=DC12VMNT,MNTIN=MNTIN,BDTEMP=BoardTemp,ENVTEMP=ENVTEMP,DEPTH=Depth,FPGAWORKING=Working_check) # 반환된 데이터 UART 송신


import time
from machine import ADC,Pin,UART

class TM_Pico:
    def __init__(self):
        self.SELA = 0#핀 초기 설정 값 0번은 LOW 1번은 HIGH
        self.SELB = 0#핀 초기 설정 값
        self.SELC = 0#핀 초기 설정 값
        self.DSPON = 1#핀 초기 설정 값
        self.TRXON = 1#핀 초기 설정 값
        self.TRXCON = 1#핀 초기 설정 값
       
        self.sela = Pin(10,mode=Pin.OUT,value=self.SELA) # SELA와 연동된 GPIO
        self.selb = Pin(11,mode=Pin.OUT,value=self.SELB) # SELB와 연동된 GPIO
        self.selc = Pin(12,mode=Pin.OUT,value=self.SELC) # SELC와 연동된 GPIO
        self.ADC_DC12VMNT = ADC(27)#ADB가 연동된 GPIO ADC로 인가 12BIT 출력 0~65535
        self.DC12VMNT = 0
        
        self.tx1 = 0
        self.TRX_CON = 0
        self.rx1 = 0
        self.baud = 0
        self.RX_Data = []
        self.result = []
        
    def RS232WRITE(self,DC12VMNT=0,Counsum_i=0, ENVTEMP=0, DEPTH=0, ROLL=0, PITCH=0):
        self.tx1 = Pin(4)
        self.rx1 = Pin(5)
        self.baud = 9600

        self.uart2 = UART(1, baudrate=self.baud, tx=self.tx1, rx=self.rx1)
        self.uart2.init(self.baud,bits=8,parity=None,stop=1)
        
        RSDAT = f'{DC12VMNT},{Counsum_i},{ENVTEMP},{DEPTH},{ROLL},{PITCH}\n'
        
        self.uart2.write(RSDAT)        
    def MUX_Check(self):
        Pin(11,mode=Pin.OUT,value=1)#SELB에 1인가
        DC12VMNT = (46/10)*(3.3/65536)*self.ADC_DC12VMNT.read_u16()#VALUE가 1일 때 DC12VMNT 출력 해당 같은 경우 12V로 출력 하기 때문에 12로 계산
        time.sleep(0.1)
#         print(DC12VMNT)
        return DC12VMNT

    def RS485READ(self,tx1=Pin(0),TRX_CON=Pin(22,mode=Pin.OUT),rx1=Pin(1),baud=115200):
        self.tx1 = tx1
        self.TRX_CON = TRX_CON
        self.TRX_CON.value(0)
        self.rx1 = rx1
        self.baud = baud
        self.uart1 = UART(0, baudrate=self.baud, tx=self.tx1, rx=self.rx1,timeout=0)
        self.uart1.init(self.baud,bits=8,parity=None,stop=1)
        while True:
            if self.uart1.any():
                for i in range(2):
                    Data = self.uart1.read()
                    time.sleep(0.1)
                    self.RX_Data.extend(Data.split(b'\r'))
                for i in self.RX_Data:
                    if b'=' in i:
                        answer = i[i.index(b'=')+1:]
                        self.result.append(answer.decode())
                self.result[2],self.result[3] = self.result[3],self.result[2]
                DC12VMNT = self.MUX_Check()
                print(DC12VMNT, self.result)
                self.RS232WRITE(DC12VMNT, 0, self.result[0], self.result[1], self.result[2], self.result[3])
                self.result = []
                self.RX_Data = []
                

if __name__=='__main__':
    A = TM_Pico()
    A.RS485READ()
