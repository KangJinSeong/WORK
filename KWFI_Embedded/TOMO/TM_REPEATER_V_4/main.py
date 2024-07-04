'''
Date: 2024.07.04
Title: TM_REPEATER V4.0(라운드 로빙 방식 최적화 및 Labview GUI 호환 )
Rev: Rev1
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
 _csv: 데이터 저장 관련 모듈
'''
from multiprocessing import Process, Queue
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import time
import RPi.GPIO as GPIO
import ntplib
from datetime import datetime
import csv
import os

class TM_Repeater:
    def __init__(self):
        '''
        해양 재난 대응을 위한 3차원 해수유동 관측기술 개발 TM_Repeater 클래스\r\n
        
         _Core1: FPGA의 GPIO Port에 트리커 신호를 전달하여 송신,수신을 제어하는 코어\r\n
         _Core2: MQTT 관련된 실행 코어(Subscribe)\r\n
         _Core3: GPS 데이터 및 BDDATA 관련된 Publish 하는 코어\r\n
         _Core4: Core1에서 수집된 데이터를 MQTT Cloud에 전송하는 코어\r\n

        '''
        
        '''
        클래스 변수 선언
         _ID: FPGA ID 값
         _Q: 신호처리 세팅 값
         _Order: 신호처리 세팅 값
         _lat: GPS 데이터(경도)
         _long: GPS 데이터(위도)
         _start_minute: 라운드 로빙방식에서 시간제어를 위한 변수
         _FPGA_Temp_data: FPGA에서 수집되는 온도 변수
         _Queue4: GPSDATA(1PPS, Latitude, Longitude, Number) 관련 변수
         _Queue2: BDDATA(배터리 전원, 소모전류, 컨트롤 온도, 수온, 압력, Roll, Pitch, Number) 관련 변수
        '''
        self.ID = 0
        self.Q = 8
        self.Order = 12
        self.lat = 0
        self.long = 0
        self.start_minute = 0
        self.FPGA_Temp_data = 'None'
        self.Pico_Data = 0
        self.Queue4 = f''
        self.queue2_4 = f''
        self.Queue2 = f''

        '''
        Queue Buffer
         _SIGDATA_BUF: FPGA 신호처리된 결과 값 전달 버퍼
         _Q_Order_BUF: 신호처리 세팅 값 변경을 위한 전달 버퍼
        '''
        self.SIGDATA_BUF = Queue()
        self.Q_Order_BUF = Queue()

        '''
        내부 클래스 선언
         _UARTIP: UART 통신(PICO, FPGA)를 위한 선언 함수
         _GPSIP: GPS 상용 모듈과 통신을 위한 선언 함수
        '''
        self.UARTIP = UART_V_3.UART_HAT()
        self.GPSIP = GPS_V_3_0.GPS_HAT()

        '''
        MQTT 서버 관련 변수 선언
         _subscribe_topics: MQTT subscribe Topic 변수
         _publish_topics: MQTT Publish Topic 변수
         _broker: MQTT Broker 변수
        '''
        self.subscribe_topics = 'Core/topic1'
        self.publish_topics = 'KWFI/3D/BDDATA/Update'
        self.broker ='test.mosquitto.org'

        '''
        TRX_Controller_Swtich 관련 선언[Pin18  (A1.1.4 SWITCH B/D 회로도 J34 커넥터 핀맵)]
        '''
        self.SWEN = 24
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.SWEN, GPIO.OUT)
        GPIO.output(self.SWEN, False)
        GPIO.setwarnings(False)

        '''
        FPGAT Triger Port 관련 선언[FPGA Triger 포트 (A1.1.4 SWITCH B/D 회로도 J34 커넥터 PIN15)]
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
         _방식: 라운드 로빙 방식을 이용하여 GUI 제어 없이 단독 동작을 진행\r\n
         _첫 번째 루프: 네트워크와 동기화 된 시간을 이용하여 기존 설계된 시간동안 TRX_Controller의 전원을 제어하여 장시간 동작하게 하는 루프
          1) TRX_Controller 운용시간: 라운드 로빙방식 운용시간의 3분 전 전원 인가
          2) 라운드 로빙방식 운용시간: 매 시간 동안 10분,30분,50분에 작동 시작됨 
         _두 번째 루프: FPGA와 통신을 하며 TX, RX 작동을 제어하고 수집된 데이터를 Queue 버퍼에 저장
          1) 라운드 로빙 방식: 1-5까지 순서대로 작동하며 TX, RX를 제어한다.
          2) TRX_Controller 운용시간: 라운드 로빙방식 운용시간의 1분 전 전원인가하여 신호처리에 필요한 값을 세팅한다.
        '''
        while True:
            try:
                while True:
                    '''
                     _첫 번쨰 루프
                    '''
                    if (datetime.now().minute) >= 7 and (datetime.now().minute) < 9:
                        self.TRX_Controller_Switch(False)
                        print(f'Start 10minute')    # 디버깅을 위한 함수(차후 삭제)
                        self.start_minute = 10
                        break                                      
                    elif (datetime.now().minute) >= 27 and (datetime.now().minute) < 29:
                        self.TRX_Controller_Switch(False)
                        print(f'Start 30minute')    # 디버깅을 위한 함수(차후 삭제)
                        self.start_minute = 30
                        break
                                       
                    elif (datetime.now().minute) >= 47 and (datetime.now().minute) < 49:
                        self.TRX_Controller_Switch(False)
                        print(f'Start 50minute')    # 디버깅을 위한 함수(차후 삭제)
                        self.start_minute = 50
                        break                  
                    else:
                        time.sleep(5)
                        print(f'else -ing') # 디버깅을 위한 함수(차후 삭제)
                        self.TRX_Controller_Switch(True)
                        time.sleep(25)
                print('Core1 Loop End') # 디버깅을 위한 함수(차후 삭제)
                while True:
                    '''
                     _두 번쨰 루프
                    '''
                    if self.start_minute == (datetime.now().minute + 1) % 60:
                        '''
                         _ 만약 신호처리 세팅 값의 버퍼가 찬 경우 사용자가 GUI를 통해 변경하고자 하는 상황이기때문에
                         그에따라 신호처리 값을 FPGA에 전달하여 세팅값을 변경한다.
                        '''
                        if not self.Q_Order_BUF.empty():
                            Q_Order = self.Q_Order_BUF.get()
                            self.Q = int(Q_Order.split(',')[0])
                            self.Order = int(Q_Order.split(',')[1])
                            print(f'CORE1, Q:{self.Q}, Order:{self.Order}') # 디버깅을 위한 함수(차후 삭제)
                            '''
                             _아래의 통신 방식은 FPGA 통신 프로토콜에 의거하여 진행됨
                            '''
                            FPGA_Q = ''.join([chr(i) for i in [0x3E,0x35,0x49,int(hex(ord(str(self.Q))),16),0x0D]])
                            if self.Order == 12:
                                FPGA_Order = ''.join([chr(i) for i in [0x3E,0x35,0x57,0x3C,0x0D]])                                                     
                            elif self.Order == 10:
                                FPGA_Order = ''.join([chr(i) for i in [0x3E,0x35,0x57,0x3A,0x0D]])                                                     
                            else:
                                FPGA_Order = ''.join([chr(i) for i in [0x3E,0x35,0x57,int(hex(ord(str(self.Order))),16),0x0D]])
                            self.UARTIP.FPGA_Put_Q(FPGA_Q)
                            time.sleep(3)
                            self.UARTIP.FPGA_Put_Order(FPGA_Order)
                            time.sleep(3)                
                            

                        print(f'CORE1, Q:{self.Q}, Order:{self.Order}') # 디버깅을 위한 함수(차후 삭제)
                        for i in range(2,4):    # 현재 장비 설치 대수가 2대 이기 때무네 range(2,4) 차후 range(2,6)으로 변경 예정
                            '''
                             _FPGA_TX: 라운드 로빙 방식 운용의 따라 1번 부터 순차적으로 송신 진행 그에 따른 명령어를 FPGA에 전달한다.
                            '''
                            FPGA_TX = ''.join([chr(i) for i in [0x3E,0x35,0x53,int(hex(ord(str(i))),16),0x0D]])
                            self.UARTIP.FPGA_Put_TX(FPGA_TX)
                            print('FPGA_TEST')  # 디버깅을 위한 함수(차후 삭제)
                            while True:
                                '''
                                 _FPGA와 트리커 신호는 D F/F에서 GPS의 1PPS의 신호와 TM_Repeater 출력 신호와 동기화 되어 전달된다.
                                 _매 분 0초 부터 시작하기 위해서는 전 분 59초에 TM_Repeater의 신호가 출력되야 1PPS신호와 동기화 되어 다음 분 0초에 시작된다.
                                '''
                                if  datetime.now().second > 58:
                                    while True:
                                        print('TRX_Triger START')   # 디버깅을 위한 함수(차후 삭제)
                                        time.sleep(0.6)
                                        GPIO.output(self.TXEN, True)
                                        '''
                                         _트리거 신호 길이: 3초(HIGH, FPGA 요구 사양)
                                        '''
                                        time.sleep(3)
                                        GPIO.output(self.TXEN, False)
                                        break
                                    while (int(self.ID) != i):
                                        '''
                                         _FPGA의 ID와 순차적으로 송신 값인 i 값과 다른 경우 수신모드 이므로 그에 따른 처리 루프를 진행한다.
                                        '''                                      
                                        try:
                                            data = self.UARTIP.FPGA_Dat_analysis()
                                            print('FPGA_GET data:',data)    # 디버깅을 위한 함수(차후 삭제)
                                            '''
                                             _FPGA로부터 수신된 데이터 중 시작 데이터 값이 '(' 와 동일 한 경우 신호처리된 값으로 판단하여 아래의 루프를 진행한다.
                                             _Queue3: 'TX_Station_ID, RX_Station_ID, INDEX, SIGDATA'
                                            '''
                                            if data[0] == '(': 
                                                da = data.replace(')(', ',')
                                                data_answer = da[1:da.index(')')]                                                
                                                Queue3 = f'({i},{self.ID},{data_answer.split(",")[0]},{data_answer})'
                                                self.SIGDATA_BUF.put(Queue3)                                                
                                                break
                                        except Exception as e:
                                            pass
                                        '''
                                         _만약 신호처리된 값이 55초이내로 들어오지 않는다면 다음 루프를 위하여 해당 루프를 강제로 종료한다.
                                        '''                
                                        if datetime.now().second >= 55:
                                            print('RX Data End')    # 디버깅을 위한 함수(차후 삭제)
                                            break
                                    break
                        break
            except Exception as e:
                print('Core1 error:',e)    # 디버깅을 위한 함수(차후 삭제)
                pass

            
    def Core2(self):
        '''
        MQTT 관련된 실행 코어(Subscribe)\r\n
        (Data Protocol: STOP,Q,Order,START)
        '''
        while True:
            try:
                m = subscribe.simple(self.subscribe_topics, hostname=self.broker, retained=False)
                print(f'CORE2 Subscribe_Data: {m.payload.decode()}')  # 디버깅을 위한 함수(차후 삭제)
                result = m.payload.decode().split(',')
                if result[0] == 'Stop':
                    self.Q = result[2]
                    self.Order =result[1]
                    self.Q_Order_BUF.put(f'{self.Q},{self.Order}')
            except Exception as e:
                print(f'Core2 error: {e}')  # 디버깅을 위한 함수(차후 삭제)
    def Core3(self):
        '''
        1) GPS 데이터 및 BDDATA 관련된 Publish 하는 코어\r\n
        Data Protocol\r\n
         _queue4:(1PPS,Latitude,Longitude,Number)
         _queue2:(DSPEN,TRXPSEN,TRXCEN,MINTIN,DC12VMN,BDTEMP,ENVTEMP,PRESSURE,DSPTEMP,Number)
        '''

        while True:
            try:
                if self.ID:
                    self.lat, self.long = self.GPSIP.get_data()
                    self.Queue4 = f'On,{self.lat:.8f},{self.long:.8f},{self.ID}'
                    self.Pico_Data = self.UARTIP.PICO_Dat_analysis()
                    self.Queue2 = f'{self.Pico_Data},NONE,{self.ID}'
                    self.queue2_4 = f'queue2:{self.Queue2}, queue4:{self.Queue4}'
                    print(f'Core3_Data:{self.queue2_4}') # 디버깅을 위한 함수(차후 삭제)
                    publish.single(topic=self.publish_topics, payload=self.queue2_4, hostname=self.broker, keepalive=0)
                    '''
                     _MQTT_Publish를 안정하게 하기 위한 시간 지연 값(시험을 통한 도출) -> 차후 수정 필요
                    '''
                    time.sleep(3*self.ID)
            except Exception as e:
                print(f'Core3 error: {e}')
                
    def Core4(self):
        '''
        1) Core1에서 수집된 데이터를 MQTT Cloud에 전송하는 코어\r\n
        '''
        while True:
            try:
                '''
                 _Core1에서 FPGA로 부터 수집된 데이터의 버퍼가 찬 경우 실핸한다.
                '''
                if not self.SIGDATA_BUF.empty():
                    data = self.SIGDATA_BUF.get()
                    Pico_data = self.UARTIP.PICO_Dat_analysis()
                    self.FPGA_Temp_data = self.UARTIP.FPGA_Put_Temp()
                    self.lat, self.long = self.GPSIP.get_data()
                    Queue4 = f'On,{self.lat:.8f},{self.long:.8f},{self.ID}'                    
                    print('Pico_data:', Pico_data)  # 디버깅을 위한 함수(차후 삭제)
                    print('FPGA_Temp_data:', self.FPGA_Temp_data)   # 디버깅을 위한 함수(차후 삭제)
                    print('RX Data:', data) # 디버깅을 위한 함수(차후 삭제)

                    '''
                     _GUI와의 데이터 프로토콜에 의거하여 데이터 포맷 변경
                    '''
                    Queue2 = f'{Pico_data},{self.FPGA_Temp_data},{self.ID}'
                    queue2_3_4 = f'queue2:{Queue2}, queue3:{data}, queue4:{Queue4}'                    
                    '''
                     _ MQTT Cloud 안정을 위한 3번의 송신(시험을 통한 도출) -> 차후 수정 필요
                    '''
                    for i in range(0,3):
                        publish.single(topic=self.publish_topics, payload=queue2_3_4, hostname=self.broker, keepalive=0)
                        time.sleep(3*self.ID)

                    '''
                     _수집된 데이터를 통신으로 잃어버릴 수 있는 경우가 있기 때문에 해당 데이터는 SD카드에 저장되어 유실상황을 방지한다.
                    '''    
                    now = datetime.now()
                    formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
                    result = data.split(',')
                    result[0] = result[0][1]
                    
                    if not os.path.exists('./CSV_Data'):
                        os.makedirs('./CSV_Data')
                    if not os.path.exists('./CSV_Data'+f"/{now.year}년"):
                        os.makedirs('./CSV_Data'+f"/{now.year}년")
                    if not os.path.exists('./CSV_Data'+f"/{now.year}년"+f"/{now.month}월"):
                        os.makedirs('./CSV_Data'+f"/{now.year}년"+f"/{now.month}월")
                    if not os.path.exists('./CSV_Data'+f"/{now.year}년"+f"/{now.month}월"+ f"/{now.day}일"):
                        os.makedirs('./CSV_Data'+f"/{now.year}년"+f"/{now.month}월"+ f"/{now.day}일")
                    path = './CSV_Data'+f"/{now.year}년"+f"/{now.month}월"+ f"/{now.day}일"
                                      
                    file_path = path + f'/Result_{formatted_now}_{result[0]}_Station_{result[1]}_Station.csv'
                    with open(file_path, mode='w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerows([result])
            except Exception as e:
                print(f'Core4 error: {e}')
        
        
        

if __name__=='__main__':
    '''
    TM_Repeater Main Loop
     1) 클래스 선언(작성된 함수 호출)
     2) TRX_Controller 메인 전원을 OFF/ON (초기화)
     3) NTP_SYNC 함수 호출로 네트워크 동기화 진행
     4) GUI Wake MQTT 신호 대기(장비 충전 시간 확보)
     5) Core1~4 실행
    '''
    A = TM_Repeater()

    A.TRX_Controller_Switch(True)
    time.sleep(3)
    A.TRX_Controller_Switch(False)
    time.sleep(3)
    while True:
        if A.NTP_SYNC():
            print(f'해당 장비의 ID: {A.FPGA_Version_info()}')
            break
    while True:
        m = subscribe.simple('Core/topic1', hostname='test.mosquitto.org', retained=False)
        print(f'System Subscribe_Data: {m.payload.decode()}')
        break
    while True:
        print(f'TM_Repeater_ID_2: Start!!')
        p1 = Process(target=A.Core1, args=())
        p2 = Process(target=A.Core2, args=())
        p3 = Process(target=A.Core3, args=())
        p4 = Process(target=A.Core4, args=())
        p1.start()
        p2.start()
        p3.start()
        p4.start()
        p1.join()
        p2.join()
        p3.join()
        p4.join()
                

