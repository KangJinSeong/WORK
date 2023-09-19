'''
Date: 2023.03.28
Title: TM_Repeater UART 통신 관련 함수
By: Kang Jin seong
'''
import serial   # 시리얼 통신 관련 모듈
import RPi.GPIO as GPIO # 라즈베리파이 포트 제어 관련 모듈

class UART_HAT: 
    def __init__(self): # 클래스 함수 초기 설정 값 선언 
        self.PICO_baudreate = 9600
        self.PICO_PORT = '/dev/ttyAMA3' # Pin 7: TXD2, Pin 29: RXD2(A1.1.2 POWER B/D 회로도 J27 커넥터 핀맵)
        self.PICO_UART = serial.Serial(self.PICO_PORT, self.PICO_baudreate, timeout = 5)
        self.PICO_EN = 27   # Pin13  (A1.1.2 POWER B/D 회로도 J22 커넥터 핀맵)
        self.FPGA_baudreate = 115200
        self.FPGA_PORT = '/dev/ttyAMA1' # Pin 27: TXD1, Pin 28: RXD1(A1.1.2 POWER B/D 회로도 J27 커넥터 핀맵)
        self.FPGA_UART = serial.Serial(self.FPGA_PORT, self.FPGA_baudreate, timeout= 5)
        self.FPGA_EN = 11   # Pin23  (A1.1.2 POWER B/D 회로도 J25 커넥터 핀맵)
        self.FPGA_Version = ''.join([chr(i) for i in [0x3E,0x35,0x40,0x30,0x0D]])   # FPGA Version 프로토콜 변수
        self.FPGA_Temp = ''.join([chr(i) for i in [0x3E,0x35,0x54,0x30,0x0D]])  # FPGA 온도 프로토콜 변수
        GPIO.setmode(GPIO.BCM)  # GPIO 핀 모드 (BCM)
        GPIO.setup(self.PICO_EN, GPIO.OUT)  # GPIO 출력모드
        GPIO.setup(self.FPGA_EN, GPIO.OUT)
        GPIO.output(self.PICO_EN, False)    # GPIO 초기값 0
        GPIO.output(self.FPGA_EN, False)
        GPIO.setwarnings(False) # GPIO Warnings 출력 해제
    def PICO_Dat_analysis(self):    # TRX_Controller Pico 보드 UART 수신 관련 함수
        data = self.PICO_UART.readline()[:-1]   # Pico 데이터 읽기
        if data == b'':
            data = b'0,0,0,0,0,0,0,0,0'
        return data # 데이터 종류: b''
    def FPGA_ECO_Dat_analysis(self):    # FPGA 보드 ECO UART 수신 관련 함수
        data = self.FPGA_UART.readline()    # FPGA 데이터 읽기
        print(data)
        Data = data.decode()    # 바이너리 데이터 디코딩
        return Data # 데이터 종류: ''
    def FPGA_Dat_analysis(self):    # FPGA 보드 UART 수신 관련 함수
        data = self.FPGA_UART.readline()    # FPGA 데이터 읽기
        Data = data.decode()    # 바이너리 데이터 디코딩
        return Data # 데이터 종류: ''
    def FPGA_Put_Version(self):    # FPGA 보드 버전 정보 확인 관련 함수
        GPIO.output(self.FPGA_EN, True) # TX Mode 설정(A1.1.2 POWER B/D 회로도 U2 MAX3221) 
        self.FPGA_UART.write(self.FPGA_Version.encode())    # FPGA 보드 UART 송신
        GPIO.output(self.FPGA_EN, False)    # RX Mode 설정(A1.1.2 POWER B/D 회로도 U2 MAX3221) 
    def FPGA_Put_Temp(self):    # FPGA 보드 온도 정보 확인 관련 함수
        GPIO.output(self.FPGA_EN, True) # TX Mode 설정(A1.1.2 POWER B/D 회로도 U2 MAX3221) 
        self.FPGA_UART.write(self.FPGA_Temp.encode())   # FPGA 보드 UART 송신
        GPIO.output(self.FPGA_EN, False)    # RX Mode 설정(A1.1.2 POWER B/D 회로도 U2 MAX3221) 
        data = self.FPGA_Dat_analysis() # FPGA 보드 UART 수신 관련 함수
        print(data)
        try:
                if data != '':       
                    data = data.split('=')  # 수신데이터 분석
                    data = data[1][0:-1]
                else:
                    data = '0'
        except:
                data = '0'
        return data
    def FPGA_Put_TX(self, FPGA_TX): # FPGA 송신 설정 명렁어 송신(UART)
        GPIO.output(self.FPGA_EN, True) # TX Mode 설정(A1.1.2 POWER B/D 회로도 U2 MAX3221) 
        self.FPGA_UART.write(str(FPGA_TX).encode()) # FPGA 보드 UART 송신
        GPIO.output(self.FPGA_EN, False)    # RX Mode 설정(A1.1.2 POWER B/D 회로도 U2 MAX3221)

if __name__ == "__main__":  # Main 함수 실행 루틴
        A = UART_HAT()
        print(A.FPGA_Put_Temp())
