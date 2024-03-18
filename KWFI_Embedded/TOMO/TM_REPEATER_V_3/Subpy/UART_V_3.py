'''
Date: 2024.02.21
Title: TM_Repeater UART 통신 관련 함수 Ver.3
By: Kang Jin seong
'''
import serial   # 시리얼 통신 관련 모듈
import RPi.GPIO as GPIO # 라즈베리파이 포트 제어 관련 모듈
import time

class UART_HAT:

    def __init__(self): # 클래스 함수 초기 설정 값 선언 
        '''
        TM_Repeater 와 Pico Board  및 FPGA 와  UART 통신을 위한 클래스\r\n
        PICO Setting:\r\n
        _Baudrate: 9600
        _PORT: '/dev/ttyAMA3'[Pin 7: TXD2, Pin 29: RXD2(A1.1.2 POWER B/D 회로도 J27 커넥터 핀맵)]
        _EN: 27\r\n
        FPGA Setting:\r\n
        _Baudrate: 115200
        _PORT: '/dev/ttyAMA1' [Pin 27: TXD1, Pin 28: RXD1(A1.1.2 POWER B/D 회로도 J27 커넥터 핀맵)]
        _EN: 11\r\n
        GPIO Setting:\r\n
        _GPIO mode: BCM
        _GPIO setup: OUT
        _GPIO output: False
        '''
        
        '''
        GPIO Setting
        '''
        self.PICO_EN = 27
        self.FPGA_EN = 11
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PICO_EN, GPIO.OUT)
        GPIO.setup(self.FPGA_EN, GPIO.OUT)
        GPIO.output(self.PICO_EN, False)
        GPIO.output(self.FPGA_EN, False)
        GPIO.setwarnings(False)
        '''
        Board Setting
        '''
        self.PICO_baudreate = 9600
        self.PICO_PORT = '/dev/ttyAMA3'
        self.PICO_UART = serial.Serial(self.PICO_PORT, self.PICO_baudreate, timeout = 5)
        self.FPGA_baudreate = 115200
        self.FPGA_PORT = '/dev/ttyAMA1'
        self.FPGA_UART = serial.Serial(self.FPGA_PORT, self.FPGA_baudreate, timeout= 5)
        '''
        FPGA DATA PROTOCOL
        '''        
        self.FPGA_Version = ''.join([chr(i) for i in [0x3E,0x35,0x40,0x30,0x0D]])
        self.FPGA_Temp = ''.join([chr(i) for i in [0x3E,0x35,0x54,0x30,0x0D]])

    def PICO_Dat_analysis(self):
        '''
        TRX_Controller Pico 보드 UART 수신 관련 함수
         _Input: None
         _Return: Data(문자열)
        '''
        data = self.PICO_UART.readline()   # Pico 데이터 읽기
        if not data:
            data = b'1,2,3,4,5,6,7,8'
        return data.decode()[:-3]

    def FPGA_Dat_analysis(self):
        '''
        FPGA 보드 UART 수신 관련 함수
         _Input: None
         _Return: Data(문자열)
        '''
        data = self.FPGA_UART.readline()
        return data.decode()
    
    def FPGA_Put_Version(self):
        '''
        FPGA 보드 버전 정보 확인 관련 함수\r\n
        FPGA_EN을 HIGH 설정 후 데이터 프로토콜에 맞춰 FPGA Version 정보 송신\r\n
        (A1.1.2 POWER B/D 회로도 U2 MAX3221)\r\n
         _Input: None
         _Return: ID
        '''
        while True:
            try:
                GPIO.output(self.FPGA_EN, True) 
                self.FPGA_UART.write(self.FPGA_Version.encode())
                GPIO.output(self.FPGA_EN, False)
                result = self.FPGA_Dat_analysis().split('=')
                print(f'Version_RX_Data: {result}')
                if 'Correlator_ID ' in result :
                     ID = int(result[-1])      
                     return ID
            except Exception as e:
                pass
                

    def FPGA_Put_Temp(self):
        '''
        FPGA 보드 온도 정보 확인 관련 함수
        FPGA_EN을 HIGH 설정 후 데이터 프로토콜에 맞춰 FPGA TEMP 정보 송신\r\n
        (A1.1.2 POWER B/D 회로도 U2 MAX3221)\r\n
         _Input: None
         _Return: TEMP
        '''
        while True:
            try:
                GPIO.output(self.FPGA_EN, True)
                self.FPGA_UART.write(self.FPGA_Temp.encode())
                GPIO.output(self.FPGA_EN, False)
                data = self.FPGA_Dat_analysis()
                return int(data.split('=')[-1])
            except Exception as e:
                pass  
    def FPGA_Put_TX(self, FPGA_TX):
        '''
        FPGA 송신 설정 명렁어 송신(UART)
        FPGA_EN을 HIGH 설정 후 데이터 프로토콜에 맞춰 FPGA TX 정보 송신\r\n
        (A1.1.2 POWER B/D 회로도 U2 MAX3221)\r\n
         _Input: None
         _Return: >5S + ID
        '''
        GPIO.output(self.FPGA_EN, True)
        self.FPGA_UART.write(str(FPGA_TX).encode())
        GPIO.output(self.FPGA_EN, False)       
        
#         while True:
#             GPIO.output(self.FPGA_EN, True)
#             self.FPGA_UART.write(str(FPGA_TX).encode())
#             GPIO.output(self.FPGA_EN, False)
#             data = self.FPGA_Dat_analysis()
#             print(data)
#             if data == ('>5S' + f'{ID}'+'\r'):
#                 break
    def FPGA_Put_Order(self, FPGA_Order):
        '''
        FPGA Order 설정 명렁어 송신(UART)
        FPGA_EN을 HIGH 설정 후 데이터 프로토콜에 맞춰 FPGA TX 정보 송신\r\n
        (A1.1.2 POWER B/D 회로도 U2 MAX3221)\r\n
         _Input: None
         _Return: >5W + Order
        '''
        GPIO.output(self.FPGA_EN, True)
        self.FPGA_UART.write(str(FPGA_Order).encode())
        GPIO.output(self.FPGA_EN, False)
        for p in range(2):  # FPGA Triger 포트 출력 한경우 FPGA로부터 수신 받은 데이터 처리 루틴 
            try:
                trash_data = self.FPGA_Dat_analysis()
                print('Trash_data :',trash_data)
            except Exception as e:
                pass       
#         while True:
#             GPIO.output(self.FPGA_EN, True)
#             self.FPGA_UART.write(str(FPGA_Order).encode())
#             GPIO.output(self.FPGA_EN, False)
#             data = self.FPGA_Dat_analysis()
#             print(data)
#             if data == ('>5W' + f'{order}'+'\r'):
#                 break           
    def FPGA_Put_Q(self, FPGA_Q):
        '''
        FPGA Q 설정 명렁어 송신(UART)
        FPGA_EN을 HIGH 설정 후 데이터 프로토콜에 맞춰 FPGA TX 정보 송신\r\n
        (A1.1.2 POWER B/D 회로도 U2 MAX3221)\r\n
         _Input: None
         _Return: >5I + Q
        '''
        GPIO.output(self.FPGA_EN, True)
        self.FPGA_UART.write(str(FPGA_Q).encode())
        GPIO.output(self.FPGA_EN, False)
        for p in range(2):  # FPGA Triger 포트 출력 한경우 FPGA로부터 수신 받은 데이터 처리 루틴 
            try:
                trash_data = self.FPGA_Dat_analysis()
                print('Trash_data :',trash_data)
            except Exception as e:
                pass        
#         while True:
#             GPIO.output(self.FPGA_EN, True)
#             self.FPGA_UART.write(str(FPGA_Q).encode())
#             GPIO.output(self.FPGA_EN, False)
#             data = self.FPGA_Dat_analysis()
#             print(data)
#             if data == ('>5I' + f'{Q_value}'+'\r'):
#                 break    

if __name__ == "__main__":  # Main 함수 실행 루틴
        A = UART_HAT()
#         A.FPGA_Put_Q(''.join([chr(i) for i in [0x3E,0x35,0x49,int(hex(ord(str(8))),16),0x0D]]))
        print(A.PICO_Dat_analysis())
        


