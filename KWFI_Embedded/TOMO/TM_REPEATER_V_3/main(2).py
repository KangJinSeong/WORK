'''
Date: 2024.02.21
Title: TM_REPEATER V3.0(라운드 로빙 방식 최적화 및 Labview GUI 호환 )
By: Kang Jin seong
'''

'''
생성한 함수\r\n
 _GPS_V_3_0: GPS 모듈 관련한 함수
 _UART_V_3: 통신 관련한 함수
'''
from Subpy import GPS_V_3_0
from Subpy import UART_V_3

'''
Python 함수\r\n
 _Process, Queue : 멀티 프로세싱 관련 함수
 _Subcribe: MQTT 수신 관련 모듈
 _Publish: MQTT 송신 관련 모듈
 _time: 라즈베리파이 시간 관련 모듈
 _RPi.GPIO: 포트 제어 관련 모듈
 _ntplib: 네트워크 시간 동기화 관련 모듈
 _datetime: 날짜 관련 모듈
'''
from multiprocessing import Process, Queue
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import time
import RPi.GPIO as GPIO
import ntplib
from datetime import datetime

class TM_Repeater:
    def __init__(self):
        '''
        해양 재난 대응을 위한 3차원 해수유동 관측기술 개발 TM_Repeater 클래스\r\n
        
         _Core1:
         _Core2:
         _Core3:
         _Core4:
        '''
        
        '''
        클래스 변수 선언
        '''
        self.ID = 0
        self.Q = 8
        self.Order = 12
        self.lat = 0
        self.long = 0
        '''
        Queue Buffer 변수
        '''

        self.SIGDATA_BUF = Queue()

        '''
        내부 클래스 선언
        '''
        self.UARTIP = UART_V_3.UART_HAT()
        self.GPSIP = GPS_V_3_0.GPS_HAT()
        '''
        MQTT 서버 관련 변수 선언
        '''
        self.subscribe_topics = 'Core/topic1'
        self.publish_topics = 'KWFI/3D/BDDATA/Update'
        self.broker ='test.mosquitto.org'
        '''
        TRX_Controller_Swtich 관련 변수 선언[Pin18  (A1.1.4 SWITCH B/D 회로도 J34 커넥터 핀맵)]
        '''
        self.SWEN = 24
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.SWEN, GPIO.OUT)
        GPIO.output(self.SWEN, False)
        GPIO.setwarnings(False)
        '''
        FPGAT Triger Port 관련 변수 선언[FPGA Triger 포트 (A1.1.4 SWITCH B/D 회로도 J34 커넥터 PIN15)]
        '''
        self.TXEN = 22
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.TXEN, GPIO.OUT)
        GPIO.output(self.TXEN, False)
        
    def FPGA_Version_info(self):
        '''
        FPGA의 Version 확인을 위한 함수
         _Input: None
         _Return: ID
        '''
        self.ID = self.UARTIP.FPGA_Put_Version()
        return self.ID
    
    def TRX_Controller_Switch(self, EN):
        '''
        TRX_Controller의 메인전원을 컨트롤 하는 함수(릴레이 스위치 -> V2.0 트랜지스터 방향 뒤집어짐)\r\n
         _True: TRX COntroller 전원 OFF
         _Input: EN
         _Return: None
        '''
        if EN:
           GPIO.output(self.SWEN, True)
        else:
            GPIO.output(self.SWEN, False)

    def NTP_SYNC(self):
        '''
        Raspberry pi의 전원이 켜졌을 떄의 네트워크 시간동기화를 위한 함수\r\n
         _NTP_SYNC_ACK: 네트워크 시간동기화가 완료 됬을 떄의 확인을 위한 Flag 변수
         _Input: None
         _Return: NTP_SYNC_ACK 
        '''
        NTP_SYNC_ACK = False
        while True:
            try:
                '''
                ntplib.NTPClient(): NTP 서버의 Connet
                ntp_client.request('time.windows.com'): 한국 Time의 Request 요청
                int(response.offset) == 0 : 네트워크 시간과 Raspberry pi의 시간의 Offset이 0인 경우 동기화 완료
                '''
                ntp_client = ntplib.NTPClient()
                response = ntp_client.request('time.windows.com')
                if int(response.offset) == 0:
                    NTP_SYNC_ACK = True
                    return NTP_SYNC_ACK
                time.sleep(1)    
            except Exception as e:
                pass
    def Core1(self):
        '''
        FPGA의 GPIO Port에 트리커 신호를 전달하여 송신,수신을 제어하는 코어\r\n
         _방식: 라운드 로빙 방식을 이용하여 GUI 제어 없이 단독 동작을 진행
        '''
        while True:
            try:
                pass

            except Exception as e:
                print('Core1 error:',e)    # 에러 발생 시 에러를 표시하고 다시 원 코드로 돌아간다.

            
    def Core2(self):
        '''
        MQTT 관련된 실행 코어(Subscribe)\r\n
        (Data Protocol: STOP,Q,Order,START)
        '''
        while True:
            try:
                m = subscribe.simple(self.subscribe_topics, hostname=self.broker, retained=False)
                print(f'Subscribe_Data: {m.payload.decode()}')
                result = m.payload.decode().split(',')
                self.Q = result[2]
                self.Order =result[1]           
            except Exception as e:
                print(f'Core2 error: {e}')
    def Core3(self):
        '''
        1) GPS 데이터 및 BDDATA 관련된 Publish 하는 코어\r\n
        2) SIGDATA 가 존재하는 경우 Publish 하는 코어\r\n
        (3초에 한번 씩 GPS Data, BDDATA 를 수집하여 Publish 하는 코어)\r\n
        Data Protocol\r\n
         _queue4:(1PPS,Latitude,Longitude,Number)
         _queue2:(DSPEN,TRXPSEN,TRXCEN,MINTIN,DC12VMN,BDTEMP,ENVTEMP,PRESSURE,DSPTEMP,Number)
         _queue3:(SIGDATA)
        '''
        while True:
            try:
                if self.ID:
                    self.lat, self.long = self.GPSIP.get_data()
                    Queue4 = f'On,{self.lat:.8f},{self.long:.8f},{self.ID}'
                    Pico_Data = self.UARTIP.PICO_Dat_analysis()
                    Queue2 = f'{Pico_Data},None,{self.ID}'
                    queue2_4 = f'queue2:{Queue2}, queue4:{Queue4}'
                    print(f'Core3_Data:{queue2_4}')
                    publish.single(topic=self.publish_topics, payload=queue2_4, hostname=self.broker)
                    time.sleep(2)

            except Exception as e:
                print(f'Core3 error: {e}')
        
        
        

if __name__=='__main__':
    A = TM_Repeater()
    while True:
        if A.NTP_SYNC():
            print(f'해당 장비의 ID: {A.FPGA_Version_info()}')
            break
    while True:
        print(f'TM_Repeater_ID_3: Start!!')
        p2 = Process(target=A.Core2, args=())
        p3 = Process(target=A.Core3, args=())
        p2.start()
        p3.start()
        p2.join()
        p3.join()
                
