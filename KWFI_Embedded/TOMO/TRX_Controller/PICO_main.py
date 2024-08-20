'''
Date: 2024.08.20
Title: PICO V4.0(센서인터페이스 보드 최적화 및 데이터 프로토콜 변경 확인 )
Rev: Rev1
By: Kang Jin seong
'''
'''
Python 함수\r\n
 _time : 시간 지연 딜레이 관련 함수
 _machine(ADC): DC12VMNT 관련 메인 전원 측정 관련 함수
 _machine(PIN): GPIO 제어 관련 함수 
 _machine(UART): UART 제어 관련 함수

'''
import time
from machine import ADC,Pin,UART



class TM_Pico:
    def __init__(self):
        '''
            해양 재난 대응을 위한 3차원 해수유동 관측기술 개발 PICO 클래스\r\n
            
             _RS232WRITE: TM_Repeater 와 통신을 위한 내부 함수(Baudrate: 115200)\r\n
             _MUX_Check: 메인전원 12VDC 확인을 위한 내부 함수\r\n
             _RS485READ: 센서 인터페이스 보드와 통신을 위한 내부 함수\r\n
        '''
        
        '''
            클래스 변수 선언
             1) MUX_Check 관련 함수 설정 값\r\n
                 _self.SELA: 핀 초기 설정 값 0번은 LOW 1번은 HIGH
                 _self.SELB: 핀 초기 설정 값
                 _self.SELC: 핀 초기 설정 값
                 _self.DSPON: 핀 초기 설정 값
                 _self.TRXON: 핀 초기 설정 값
                 _self.TRXCON: 핀 초기 설정 값
                 _self.sela: SELA와 연동된 GPIO
                 _self.selb: SELB와 연동된 GPIO
                 _self.selc: SELC와 연동된 GPIO
                 _self.ADC_DC12VMNT: ADB가 연동된 GPIO ADC로 인가 12BIT 출력 0~65535
                 _self.DC12VMNT: 전원 변수
             2) UART 관련 함수 설정 값\r\n
                 _self.tx1: TX Pin 설정 값
                 _self.TRX_CON: TX,RX 설정 관련 변수
                 _self.rx1: RX Pin 설정 값
                 _self.baud: Baudrate 관련 변수
             3) RS485 관련 함수 설정 값\r\n
                 _self.RX_Data: 센서 인터페이스보드로 수신된 데이터 관련 변수
                 _self.result: 온도 관련 최종 출력 변수
                 _self.PITCH: 자세 관련 출력 변수
                 _self.ROLL: 자세 관련 출력 변수
                 _self.RTH: 센서인터페이스보드로 수신된 온도센서 저항 값 관련 변수
                 _self.PA: 센서인터페이스보드로 수신된 압력센서 전압 값 관련 변수
                 _self.temp_ohms: 센서인터페이스보드 온도센서 데이터시트 저항 값
                 _self.temp_temp: 센서인터페이스보드 온도센서 데이터시트 온도 값
                 _self.temp: 데이터시트 온도 저장 값 관련 변수
                 _self.step: 온도 변화량 관련 변수
                 _self.low: 온도변화 관련 최소치 저항값 변수
                 _self.up = 온도변화 관련 최대치 저항값 변수
                 _self.PA_answer: 압력 관련 파스칼 변환 관련 변수
                 _self.depth: 압력 관련 최종 출력 변수
        '''
        self.SELA = 0
        self.SELB = 0
        self.SELC = 0
        self.DSPON = 1
        self.TRXON = 1
        self.TRXCON = 1
       
        self.sela = Pin(10,mode=Pin.OUT,value=self.SELA)
        self.selb = Pin(11,mode=Pin.OUT,value=self.SELB)
        self.selc = Pin(12,mode=Pin.OUT,value=self.SELC)
        self.ADC_DC12VMNT = ADC(27)
        self.DC12VMNT = 0
        
        self.tx1 = 0
        self.TRX_CON = 0
        self.rx1 = 0
        self.baud = 0
        self.RX_Data = []
        self.result = 0
        self.PITCH = 0
        self.ROLL = 0
        self.RTH =  0
        self.PA = 0
        self.temp_ohms = [336052, 314512, 294487, 275863, 258533, 242399, 227373, 213371, 200318, 188144, 176786, 166183, 156280, 147029, 138382, 130296, 122732, 115656, 109025, 102817, 97000, 91547, 86433, 81636, 77134, 72907, 68937, 65206, 61700, 58403, 55301, 52383, 49636, 47049, 44612, 42315, 40150, 38109, 36183, 34366, 32650, 31030, 29500, 28054, 26687, 25395, 24172, 23016, 21921, 20884, 19903, 18973, 18092, 17257, 16465, 15714, 15001, 14324, 13682, 13073, 12493, 11943, 11420, 10923, 10450, 10000, 9572, 9164, 8777, 8407, 8056, 7721, 7401, 7097, 6807, 6530, 6266, 6014, 5773, 5544, 5325, 5115, 4915, 4724, 4541, 4367, 4200, 4040, 3887, 3741, 3601, 3467, 3338, 3215, 3098, 2985, 2877, 2773, 2673, 2578, 2487, 2399, 2315, 2234, 2156, 2082, 2010, 1942, 1876, 1812, 1751, 1693, 1636, 1582, 1530, 1480, 1431, 1385, 1340, 1297, 1256, 1216, 1177, 1140, 1104, 1070, 1037, 1005, 974, 944, 916, 888, 861, 835, 810, 786, 763, 741, 719, 698, 678, 658, 640, 621, 604, 587, 570, 554, 539, 524, 509, 495, 482, 469, 456, 444, 432, 420, 409, 398, 388, 378, 368, 358, 349, 340]
        self.temp_temp = [-40, -39, -38, -37, -36, -35, -34, -33, -32, -31, -30, -29, -28, -27, -26, -25, -24, -23, -22, -21, -20, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125]
        self.temp = 0
        self.step = 0
        self.low = 0
        self.up = 0
        self.PA_answer = 0
        self.depth = 0

        
    def RS232WRITE(self,DC12VMNT=0,Counsum_i=0, ENVTEMP=0, DEPTH=0, ROLL=0, PITCH=0, BoardTemp=0):
        '''
            TM_Repeater 와 통신을 위한 내부 함수(Baudrate: 115200)\r\n
             _Input:
              _DC12VMNT: 전원
              _Counsum_i: 소모전류
              _ENVTEMP: 온도(센서인터페이스보드)
              _DEPTH: 압력(센서인터페이스보드)
              _ROLL: 자세센서(센서인터페이스보드)
              _PITCH: 자세센서(센서인터페이스보드)
              _BoardTemp: 인터페이스보드 온도센서(현재 사용 X)
             _Return: 0
        '''
        self.tx1 = Pin(4)
        self.rx1 = Pin(5)
        self.baud = 115200

        self.uart2 = UART(1, baudrate=self.baud, tx=self.tx1, rx=self.rx1)
        self.uart2.init(self.baud,bits=8,parity=None,stop=1)
        
        RSDAT = f'{DC12VMNT},{Counsum_i},{ENVTEMP},{DEPTH},{ROLL},{PITCH}\n'
        
        self.uart2.write(RSDAT)
        return 0
    
    def MUX_Check(self):
        '''
            센서 인터페이스 보드와 통신을 위한 내부 함수\r\n
             _Input:메인전원 12VDC 확인을 위한 내부 함수\r\n
             _Return: DC12VMNT
        '''
        Pin(11,mode=Pin.OUT,value=1)
        DC12VMNT = (46/10)*(3.3/65536)*self.ADC_DC12VMNT.read_u16()
        return DC12VMNT

    def RS485READ(self,tx1=Pin(0),TRX_CON=Pin(22,mode=Pin.OUT),rx1=Pin(1),baud=115200):
        '''
            센서 인터페이스 보드와 통신을 위한 내부 함수\r\n
             _Input:
              _self.tx1: TX Pin 설정 값
              _self.TRX_CON: TX,RX 설정 관련 변수
              _self.rx1: RX Pin 설정 값
              _self.baud: Baudrate 관련 변수
             _Return: 0
        '''
        self.tx1 = tx1
        self.TRX_CON = TRX_CON
        self.TRX_CON.value(0)
        self.rx1 = rx1
        self.baud = baud
        self.uart1 = UART(0, baudrate=self.baud, tx=self.tx1, rx=self.rx1,timeout=0)
        self.uart1.init(self.baud,bits=8,parity=None,stop=1)
        '''
            _windowsize: 배열 슬라이싱으로 2개씩 검출하기 위한 윈도우 사이즈 변수
            _step: 몇 단계의 배열 슬라이싱을 위한 변수
        '''
        windowsize = 2
        step = 1
        while True:
            try:
                if self.uart1.any():
                    '''
                        _센서 인터페이스보드로 UART 데이터를 프로토콜에 맞춰 데이터 분리 및 변수에 할당 루틴
                        
                    '''
                    Data = self.uart1.read()
                    self.RX_Data = Data.split(b'\r\n')
                    for i in self.RX_Data[2:-1:]:
                        self.result = i.split(b'=')
                        if self.result[0] == b'>P':
                            self.PITCH = self.result[1].decode()
                        elif self.result[0] == b'>R':
                            self.ROLL = self.result[1].decode()
                        elif self.result[0] == b'>RTH':
                            self.RTH = self.result[1].decode()
                        elif self.result[0] == b'>pa':
                            self.PA = self.result[1].decode()                            
                    pair = [self.temp_ohms[i:i+windowsize] for i in range(0, len(self.temp_ohms) - windowsize +1, step)] #배열 슬라이싱

                for p in pair:
                    '''
                        _센서 인터페이스보드로 부터 수신된 데이터 중 온도 데이터를 데이터시트와 비교하여 최종 출력 온도에이터로 변환 하기 위한 루틴
                         _1) 온도센서 데이터 중 저항 데이터 값을 2새씩 비교하여 현재 측정 된 온도센서(센서인터페이스보드) 저항 범위 설정
                         _2) 저항 범위가 설정이 되면 해당 값의 따른 온도 설정이 가능(예: 22도~23도 사이)
                         _3) 저항 범위를 10단계로 나누어 저항범위를 상세하게 설정(계산)
                         _4) 상세하게 나누어진 저항 범위의 따른 온도 설정(예:22.1도~22.9도)
                        
                    '''                    
                    low = p[1]
                    up = p[0]
                    if(low < float(self.RTH) <= up):
                        self.temp = self.temp_temp[self.temp_ohms.index(low)]
                        self.step = (up-low)/10
                        self.low = low
                        self.up = up
                '''
                    _저항범위를 10단계로 나누어 상세하게 설정 루틴
                '''
                if ( self.low <= float(self.RTH) < self.low + self.step ):
                    self.result = self.temp
                elif ( self.low+self.step <= float(self.RTH) < self.low + (self.step*2) ):
                    self.result = self.temp + 0.1
                elif ( self.low+(self.step*2) <= float(self.RTH) < self.low + (self.step*3) ):
                    self.result = self.temp + 0.2                    
                elif ( self.low+(self.step*3) <= float(self.RTH) < self.low + (self.step*4) ):
                    self.result = self.temp + 0.3
                elif ( self.low+(self.step*4) <= float(self.RTH) < self.low + (self.step*5) ):
                    self.result = self.temp + 0.4                    
                elif ( self.low+(self.step*5) <= float(self.RTH) < self.low + (self.step*6) ):
                    self.result = self.temp + 0.5
                elif ( self.low+(self.step*6) <= float(self.RTH) < self.low + (self.step*7) ):
                    self.result = self.temp + 0.6
                elif ( self.low+(self.step*7) <= float(self.RTH) < self.low + (self.step*8) ):
                    self.result = self.temp + 0.7
                elif ( self.low+(self.step*8) <= float(self.RTH) < self.low + (self.step*9) ):
                    self.result = self.temp + 0.8
                elif ( self.low+(self.step*9) <= float(self.RTH) < self.up ):
                    self.result = self.temp + 0.9
                elif ( float(self.RTH) >= self.up ):
                    self.result = self.temp + 1
                '''
                    _센서인터페이스보드로 부터 수신된 압력센서의 전압값을 데이터시트에 의거하여 파스칼 값으로 변환
                '''
                self.PA_answer = (float(self.PA) * 5) / 1e6
                self.depth = self.PA_answer/9816# 수심 데이터로 변환 1m:9816Pa

                DC12VMNT = self.MUX_Check()
                
                self.RS232WRITE(DC12VMNT, 0, self.result, self.depth, self.ROLL, self.PITCH)
                print(f'PITCH = {self.PITCH}, ROLL = {self.ROLL}, RTH = {self.result}, PA = {self.depth}, DC12VMNT = {DC12VMNT}')#디버깅
                time.sleep(0.5)
            except:
                return 0
            
        return 0
                

while True:
    '''
        _메인함수
    '''
    A = TM_Pico()
    A.RS485READ()


