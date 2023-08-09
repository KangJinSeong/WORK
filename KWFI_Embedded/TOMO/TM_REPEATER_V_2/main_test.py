'''
Date: 2023.08.09
Title: TM_REPEATER V2.0
By: Kang Jin seong
'''
# from Subpy import GPS_V_2_0 #하드웨어 조작 관련 모듈
from Subpy import UART_V_2    #UART 통신 관련 모듈
from multiprocessing import Process, Queue  # 멀티 프로세싱 관련 모듈
import paho.mqtt.subscribe as subcribe  # MQTT 수신 관련 모듈
import paho.mqtt.publish as publish     # MQTT 송신 관련 모듈
import time     # 라즈베리파이 시간 관련 모듈
import RPi.GPIO as GPIO # 라즈베리파이 포트 제어 관련 모듈
import ntplib
from time import ctime
from datetime import datetime

class TM_Repeater:
    def __init__(self):

        # ※ 클래스 변수 선언
        self.StationID = 0  # 장비 시리얼 넘버
        self.min_index = [10, 30, 50]
        self.min_index_number = 0


        # ※ 클래스 함수 내부 모듈 선언
        self.UARTIP = UART_V_2.UART_HAT() # UART 통신 관련 함수 선언

        # ※ MQTT 서버 관련 변수 선언
        self.data_topics = 'Core/test12343Demension/data'   # MQTT 제어신호 관련 토픽
        self.GPS_topics = 'Core/test12343Demension/version' # MQTT GPS 신호 관련 토픽
        self.broker ='test.mosquitto.org'   # MQTT 브로커

        # ※ TRX_Controller_Swtich 관련 변수 선언
        self.SWEN = 24  # Pin18  (A1.1.4 SWITCH B/D 회로도 J34 커넥터 핀맵)
        GPIO.setmode(GPIO.BCM)  # GPIO 핀 모드 (BCM)
        GPIO.setup(self.SWEN, GPIO.OUT) # GPIO 출력모드
        GPIO.output(self.SWEN, False)   # GPIO 초기값 0
        GPIO.setwarnings(False) # GPIO Warnings 출력 해제

    def TRX_Controller_Switch(self, EN):
        if EN:
           GPIO.output(self.SWEN, True)   # TRX COntroller 전원 OFF
        else:
            GPIO.output(self.SWEN, False)   # TRX COntroller 전원 ON

    def NTP_SYNC(self):
        NTP_SYNC_ACK = 0
        while True:
            try:
                ntp_client = ntplib.NTPClient()
                response = ntp_client.request('time.windows.com')
                print(ctime(response.tx_time))
                print('offset: {:2f} s'.format(response.offset))
                if int(response.offset) == 0:
                    NTP_SYNC_ACK = 1
                    return NTP_SYNC_ACK
                time.sleep(1)    
            except Exception as e:
                print('현재 장비 시간: {},{},{}'.format(datetime.now().hour, datetime.now().minute, datetime.now().second))
                print('NTP SYNC error: {}'.format(e))
                time.sleep(1) 

        
    def FPGA_Version_info(self):    # 장비별 시리얼 번호 얻기를 위한 함수
        while True:
            data = self.UARTIP.FPGA_Dat_analysis()  # UART 통신을 통한 데이터 분
            print(data)
            if 'Correlator_ID' in data: # 버전 정보에서 ID 값 유무를 분석
                answer = data.split('=')
                self.StationID = answer[1][1]
                State = 1
            if 'Ok' in data:
                break      
        return State, self.StationID

    def core1(self):
        while True: # 시작 모드
            for q in self.min_index:
                while True: 
                    if q == datetime.now().minute + 3:
                        self.TRX_Controller_Switch(self, 0)
                        break
                    else:
                        self.TRX_Controller_Switch(self, 1)
                        time.sleep(30000)

                while True:
                    if q == datetime.now().minute + 1:
                        for i in range(1,6):
                            FPGA_TX = ''.join([chr(i) for i in [0x3E,0x35,0x53,int(hex(ord(str(i))),16),0x0D]]) # FPGA 송신 설정 프로토콜 변수
                            self.UARTIP.FPGA_Put_TX(FPGA_TX)    # FPGA 송신 설정 명렁어 송신(UART)
                            while True:
                                if  datetime.now().second > 58:
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
                                    while (int(self.StationID) != i):  # Timezone 함수로 설정한 변수 s_id 와 FPGA로부터 얻은 stationid가 다른경우 아래 루틴 실행(수신모드)
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
                                                result = bytes(str(self.s_id),'utf-8')+b','+bytes(self.StationID,'utf-8')+b','+[Pico_data[1:] if b'\x00' in Pico_data else Pico_data][0]+b',' + bytes(FPGA_Temp_data,'utf-8')+b','+bytes(data_answer,'utf-8')
                                                print('RX Data:', result)
                                                time.sleep(int(self.StationID))
                                                publish.single(topic='Core/sendTestData1234/data',payload = result,hostname='test.mosquitto.org',keepalive= 0)  # MQTT Server로 데이터 넣기
                                                break   # 수신 루틴 종료
                                        if self.count >= 40:    # 3분 30초 경과 한 경우 수신 루틴 종료
                                            self.count = 0  # 해당 루틴 실행 횟수 초기화
                                            print('RX Data End')
                                            break   # 수신 루틴 종료
                                    break
                        break
 
        


if __name__ == "__main__":  # Main 함수 실행 루틴
    A = TM_Repeater()    # TM Repater

    while True:
        if A.NTP_SYNC():
            State, Station_ID = A.FPGA_Version_info()
            break