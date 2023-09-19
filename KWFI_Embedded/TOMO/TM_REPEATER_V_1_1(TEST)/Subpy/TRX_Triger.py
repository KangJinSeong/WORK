'''
Date: 2023.03.29
Title: Main Server로 부터 입력된 시간에 따라 TRX Controller를 구동하기 위한 Triger 신호 출력 함수(REV1)
By: Kang Jin seong
'''
import RPi.GPIO as GPIO # 라즈베리파이 포트 제어 관련 모듈
import time # 라즈베리파이 시간 관련 모듈
from datetime import datetime   # 네트워크 날짜,시간 확인 관련 모듈
from Subpy import UART_V_1_1    # UART 통신 관련 모듈
import paho.mqtt.publish as publish # MQTT 송신 관련 모듈
#from nptdms import TdmsWriter, ChannelObject
import datetime as dt
import ntplib

class TRX_TRG:
    def __init__(self): # 클래스 함수 초기 설정 값 선언 
        self.TXEN = 22  # FPGA Triger 포트 (A1.1.4 SWITCH B/D 회로도 J34 커넥터 PIN15)
        GPIO.setmode(GPIO.BCM)  # GPIO 핀 모드 (BCM)
        GPIO.setup(self.TXEN, GPIO.OUT) # GPIO 출력으로 설정
        GPIO.output(self.TXEN, False)   # 초기값 0
        GPIO.setwarnings(False) # GPIO Warnings 출력 해제
        # ※ 변수 선언
        self.s_hour = 0 # Hour
        self.s_min = 0  # Min
        self.s_interval = 0 # Interval
        self.s_id = 0   # ID
        self.count = 0  # FPGA 수신 대기 카운터 변수
        self.tt = 1
        self.second = 0
        # ※ UART 통신을 위한 모듈 선언
        self.UARTIP = UART_V_1_1.UART_HAT()
    def timezone(self,hour,min,interval,id):    # 입력 변수를 클래스 변수로 선언 관련 함수
        self.s_hour = hour
        self.s_min = min
        self.s_interval = interval
        self.s_id = id
    def Data_analysis(self, data):  # 네트워크 프로토콜 분석 관련 함수(data: 문자열 Mqtt로부터 수신 받은 데이터)
        Data = data.split(',')  # 구분자를 이용하여 데이터 분리
        print(Data) # TEST CODE
        if ('START' in Data):   # START 명령어 있다면 프로토콜에 맞춰 데이터 분리
            result = [int(i) for i in Data[1:-1]]
        else:   # START 명령어 없다면 데이터는 0으로 설정
            result = [0,0,0,0]
        return result 
    def main(self, stationid):  # Class TRX_TRG Main Function(입력값: 장비번호)
        if (self.s_hour%24) == datetime.now().hour: # Timezone 함수로 설정한 변수 값과 네트워크 동기화 된 시간 판단
            ntp_client = ntplib.NTPClient()
            response = ntp_client.request('time.windows.com')
            print('offset: {:2f} s'.format(response.offset))
            time.sleep(1)
            if (self.s_min%60) == datetime.now().minute + int(response.offset) +1:    # Timezone 함수로 설정한 변수 값과 네트워크 동기화 된 분 판단
                if self.tt:
                    FPGA_TX = ''.join([chr(i) for i in [0x3E,0x35,0x53,int(hex(ord(str(self.s_id))),16),0x0D]]) # FPGA 송신 설정 프로토콜 변수
                    self.UARTIP.FPGA_Put_TX(FPGA_TX)    # FPGA 송신 설정 명렁어 송신(UART)
                    print('FPGA_TX:', FPGA_TX)
                    self.tt = 0

                print('분:', datetime.now().minute)
                while True:
                    if  datetime.now().second > 58:
                        self.tt = 1
                        '''
                        ※ 안전코드
                        1) 네트워크 통신 불안으로 인한 timezone 함수의 실행(시간 업데이트)이 되지 않았을 경우 interval 과 관계없이 해당 분에 계속 Main 함수 실행
                        2) 해당 시간이 경과되면 s_min 변수를 -1감소 시켜 해당 분에 M ain 함수 실행 방지
                        3) 네트워크 통신 연결 대기 
                        '''
                        print('main routine ing min')
                        self.s_min = datetime.now().minute-1    # 안전코드
                        while True: # FPGA 프로토콜에 맞춰 UART 통신 및 GPIO 포트 설정
                            print('TRX_Triger START')
                            time.sleep(0.6)
                            GPIO.output(self.TXEN, True)
                            time.sleep(3)
                            GPIO.output(self.TXEN, False)
                            for i in range(2):  # FPGA Triger 포트 출력 한경우 FPGA로부터 수신 받은 데이터 처리 루틴 
                                trash_data = self.UARTIP.FPGA_Dat_analysis()
                                print('Trash_data :',trash_data)
                            break
                        while (int(stationid) != self.s_id):  # Timezone 함수로 설정한 변수 s_id 와 FPGA로부터 얻은 stationid가 다른경우 아래 루틴 실행(수신모드)
                            print('RX Data ing')
                            data = self.UARTIP.FPGA_Dat_analysis()  # FPGA로 부터 데이터 수신(UART, timeout = 5s)
                            print('FPGA_GET data:',data)
                            self.count += 1 # 해당 루틴 실행 횟수 카운터
                            if len(data) > 0:   # 데이터의 길이가 0보다 큰경우 아래 루틴 실행(데이터 수신)
                                self.count = 0  # 루틴 실행 횟수 카운터 초기화
                                if data[0] == '(':  # 데이터 프로토콜에 맞춰서 데이터 분리
                                    da = data.replace(')(', ',')
                                    data_answer = da[1:da.index(')')]          
                                    Pico_data = self.UARTIP.PICO_Dat_analysis() # TRX_Controller Pico B/D와 UART 통신
                                    FPGA_Temp_data = self.UARTIP.FPGA_Put_Temp()    # FPGA 온도 데이터 통신
                                    print('Pico_data:', Pico_data)
                                    print('FPGA_Temp_data:', FPGA_Temp_data)
                                    # 데이터 합치기: 네트워크로 받은 ID + 장비 ID + Pico 데이터 + 신호처리 데이터
                                    result = bytes(str(self.s_id),'utf-8')+b','+bytes(stationid,'utf-8')+b','+[Pico_data[1:] if b'\x00' in Pico_data else Pico_data][0]+b',' + bytes(FPGA_Temp_data,'utf-8')+b','+bytes(data_answer,'utf-8')
                                    print('RX Data:', result)
                                    time.sleep(int(stationid) * 4)
                                    publish.single(topic='Core/sendTestData1234/data',payload = result,hostname='test.mosquitto.org',keepalive= 0)  # MQTT Server로 데이터 넣기
                                    break   # 수신 루틴 종료
                            if self.count >= 40:    # 3분 30초 경과 한 경우 수신 루틴 종료
                                self.count = 0  # 해당 루틴 실행 횟수 초기화
                                print('RX Data End')
                                break   # 수신 루틴 종료
                        break


         
