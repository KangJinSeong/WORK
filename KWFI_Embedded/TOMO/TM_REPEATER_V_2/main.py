'''
Date: 2023.09.21
Title: TM_REPEATER V2.0(라운드 로빙 방식 최적화)
By: Kang Jin seong
'''
from Subpy import GPS_V_2_0 #하드웨어 조작 관련 모듈
from Subpy import UART_V_2    #UART 통신 관련 모듈

from multiprocessing import Process, Queue  # 멀티 프로세싱 관련 모듈
import paho.mqtt.subscribe as subcribe  # MQTT 수신 관련 모듈
import paho.mqtt.publish as publish     # MQTT 송신 관련 모듈
import time     # 라즈베리파이 시간 관련 모듈
import RPi.GPIO as GPIO # 라즈베리파이 포트 제어 관련 모듈
import ntplib   # 네트워크 시간 동기화 관련 모듈
from datetime import datetime   # 시간 관련 모듈

class TM_Repeater:
    def __init__(self):
        
        # ※ MQTT 데이터 Q 버퍼 선언
        self.RxData = Queue() # Core2 에서 Mqtt 클라우드로 송신을 위한 데이터 Q 버퍼선언

        # ※ 클래스 변수 선언
        self.StationID = 0  # 장비 시리얼 넘버
        self.min_index = 0  # 라운드 로빙 방식의 Default Time
        self.count = 0	# FPGA Receive wait variable

        # ※ 클래스 함수 내부 모듈 선언
        self.UARTIP = UART_V_2.UART_HAT() # UART 통신 관련 함수 선언

        # ※ MQTT 서버 관련 변수 선언
        self.data_topics = 'Core/sendTestData1234/data1'   # MQTT 데이터 신호 관련 토픽
        self.GPS_topics = 'Core/test12343Demension/version1' # MQTT GPS 신호 관련 토픽
        self.broker ='test.mosquitto.org'   # MQTT 브로커

        # ※ TRX_Controller_Swtich 관련 변수 선언
        self.SWEN = 24  # Pin18  (A1.1.4 SWITCH B/D 회로도 J34 커넥터 핀맵)
        GPIO.setmode(GPIO.BCM)  # GPIO 핀 모드 (BCM)
        GPIO.setup(self.SWEN, GPIO.OUT) # GPIO 출력모드
        GPIO.output(self.SWEN, False)   # GPIO 초기값 0
        GPIO.setwarnings(False) # GPIO Warnings 출력 해제

        # ※ FPGAT Triger Port
        self.TXEN = 22  # FPGA Triger 포트 (A1.1.4 SWITCH B/D 회로도 J34 커넥터 PIN15)
        GPIO.setmode(GPIO.BCM)  # GPIO 핀 모드 (BCM)
        GPIO.setup(self.TXEN, GPIO.OUT) # GPIO 출력으로 설정
        GPIO.output(self.TXEN, False)   # 초기값 0

    def TRX_Controller_Switch(self, EN):    # TRX_Controller의 메인전원을 컨트롤 하는 함수(릴레이 스위치 -> V2.0 트랜지스터 방향 뒤집어짐)
        if EN:
           GPIO.output(self.SWEN, True)   # TRX COntroller 전원 OFF
        else:
            GPIO.output(self.SWEN, False)   # TRX COntroller 전원 ON

    def NTP_SYNC(self): # Raspberry pi의 전원이 켜졌을 떄의 네트워크 시간동기화를 위한 함수
        NTP_SYNC_ACK = 0    # 네트워크 시간동기화가 완료 됬을 떄의 확인을 위한 Flag 변수
        while True:
            try:
                ntp_client = ntplib.NTPClient() # NTP 서버의 Connet
                response = ntp_client.request('time.windows.com')   # 한국 Time의 Request 요청
                #print(ctime(response.tx_time)) # 디버깅을 위한 코드
                #print('offset: {:2f} s'.format(response.offset))   # 디버깅을 위한 코드
                if int(response.offset) == 0:   # 네트워크 시간과 Raspberry pi의 시간의 Offset이 0인 경우 동기화 완료로 가정
                    NTP_SYNC_ACK = 1
                    return NTP_SYNC_ACK # Flag 변수를 1로 Return
                time.sleep(1)    
            except Exception as e:
                #print('현재 장비 시간: {},{},{}'.format(datetime.now().hour, datetime.now().minute, datetime.now().second))    # 디버깅을 위한 코드
                #print('NTP SYNC error: {}'.format(e))  # 디버깅을 위한 코드
                time.sleep(1) 

        
    def FPGA_Version_info(self):    # 장비별 시리얼 번호 얻기를 위한 함수
        while True:
            data = self.UARTIP.FPGA_Dat_analysis()  # UART 통신을 통한 데이터 분석
            print(data)
            if 'Correlator_ID' in data: # 버전 정보에서 ID 값 유무를 분석
                answer = data.split('=')    # 데이터 프로토콜 참조
                self.StationID = answer[1][1]
                State = 1
            if 'Ok' in data:    # 수신 데이터 중 'Ok' 가 있는 경우 데이터 완료로 가정
                break      
        return State, self.StationID    # 상태 값과 ID 값을 Return

    def core1(self):    
        while True: # 시작 모드
            try:
                while True: # 첫 번째 루프
                    print('Time Test')  # 디버깅을 위한 코드
                    '''
                    라운드 로빙 방식의 Default 값이 해당됬을 경우 self.min_index 변수에 할당
                    Default 값의 3분전부터 TRX_Controller의 전원을 인가한다
                    1분 전 부터 FPGA와 통신을 해야하기 떄문에 최대 9분사이인 경우에만 self.min_indeㅌ 변수에 할당한다
                    그 이외의 시간에는 할당하지 않기 때문에 동작을 하지 않는다. 
                    '''
                    if (datetime.now().minute ) >= 7 and (datetime.now().minute ) <=  9:    # 7분에서 9분 사이인 경우 
                        self.TRX_Controller_Switch(0)   # TRX_Controller의 메인전원을 ON
                        print('START : [10]')
                        self.min_index = 10
                        break   # 해당 시간에 들어 온경우 첫 번쨰 루프를 종료한다.
                    elif (datetime.now().minute) >= 27 and (datetime.now().minute ) <=  29:
                        self.TRX_Controller_Switch(0)
                        print('START : [30]')
                        self.min_index = 30
                        break   # 해당 시간에 들어 온경우 첫 번쨰 루프를 종료한다.
                    elif (datetime.now().minute) >= 47 and (datetime.now().minute ) <=  49:
                        self.TRX_Controller_Switch(0)
                        print('START : [50]')
                        self.min_index = 50
                        break   # 해당 시간에 들어 온경우 첫 번쨰 루프를 종료한다.
                    else:   # Default 값의 들어 오지 않은 경우 TRX_Controller의 메인전원을 OFF, 첫 번째 루프를 계속 실행한다.
                        time.sleep(10)
                        self.TRX_Controller_Switch(1)
                        time.sleep(30)
                print('end')    # 디버깅을 위한 코드

                while True: # 두 번째 루프
                    if self.min_index == datetime.now().minute + 1: # Default 값의 1분 전부터 두 번째 루프를 실행한다. 
                        '''
                        라운드 로빙 방식은 5EA 
                        '''
                        for i in range(1,6):
                            FPGA_TX = ''.join([chr(i) for i in [0x3E,0x35,0x53,int(hex(ord(str(i))),16),0x0D]]) # FPGA 송신 설정 프로토콜 변수
                            self.UARTIP.FPGA_Put_TX(FPGA_TX)    # FPGA 송신 설정 명렁어 송신(UART)
                            print('FPGA_TEST')
                            while True:
                                if  datetime.now().second > 58:
                                    while True: # FPGA 프로토콜에 맞춰 UART 통신 및 GPIO 포트 설정
                                        print('TRX_Triger START')
                                        time.sleep(0.6)
                                        GPIO.output(self.TXEN, True)
                                        time.sleep(3)
                                        GPIO.output(self.TXEN, False)
                                        for p in range(2):  # FPGA Triger 포트 출력 한경우 FPGA로부터 수신 받은 데이터 처리 루틴 
                                            try:
                                                trash_data = self.UARTIP.FPGA_Dat_analysis()
                                                print('Trash_data :',trash_data)
                                            except Exception as e:
                                                print(e)
                                        break
                                    while (int(self.StationID) != i):  # Timezone 함수로 설정한 변수 s_id 와 FPGA로부터 얻은 stationid가 다른경우 아래 루틴 실행(수신모드)
                                        print('RX Data ing')
                                        print(i)
                                        try:
                                            data = self.UARTIP.FPGA_Dat_analysis()  # FPGA로 부터 데이터 수신(UART, timeout = 5s)
                                        except Exception as e:
                                            print(e)
                                        print('FPGA_GET data:',data)
                                        self.count += 1 # 해당 루틴 실행 횟수 카운터
                                        if len(data) > 0:   # 데이터의 길이가 0보다 큰경우 아래 루틴 실행(데이터 수신)
                                            self.count = 0  # 루틴 실행 횟수 카운터 초기화
                                            if data[0] == '(':  # 데이터 프로토콜에 맞춰서 데이터 분리
                                                da = data.replace(')(', ',')
                                                data_answer = da[1:da.index(')')]
                                                data_answer_1 = data_answer.split(',')
                                                data_answer_2 = [int(i) for i in data_answer_1]
                                                data_answer_2[0] = data_answer_2[0]-2000
                                                data_answer_3 = [str(i) for i in data_answer_2]
                                                data_answer_4 = ','.join(data_answer_3)
                                                
                                                Pico_data = self.UARTIP.PICO_Dat_analysis() # TRX_Controller Pico B/D와 UART 통신
                                                FPGA_Temp_data = self.UARTIP.FPGA_Put_Temp()    # FPGA 온도 데이터 통신
                                                print('Pico_data:', Pico_data)
                                                print('FPGA_Temp_data:', FPGA_Temp_data)
                                                # 데이터 합치기: 네트워크로 받은 ID + 장비 ID + Pico 데이터 + 신호처리 데이터
                                                result = bytes(str(i),'utf-8')+b','+bytes(self.StationID,'utf-8')+b','+[Pico_data[1:] if b'\x00' in Pico_data else Pico_data][0]+b',' + bytes(FPGA_Temp_data,'utf-8')+b','+bytes(data_answer_4,'utf-8')
                                                print('RX Data:', result)
                                                self.RxData.put(result)
                                                # time.sleep(int(self.StationID))
                                                # publish.single(topic='Core/sendTestData1234/data1',payload = result,hostname='test.mosquitto.org',keepalive= 0)  # MQTT Server로 데이터 넣기
                                                break   # 수신 루틴 종료
                                        if self.count >= 11:    # 55초 경과 한 경우 수신 루틴 종료
                                            self.count = 0  # 해당 루틴 실행 횟수 초기화
                                            print('RX Data End')
                                            break   # 수신 루틴 종료
                                    break
                        break
            except Exception as e:
                print('Core1 error:',e)    # 에러 발생 시 에러를 표시하고 다시 원 코드로 돌아간다.
    def core2(self):
        while True:
            try:
                if self.StationID != 0:     # 장비 시리얼 넘버를 얻은 후 아래 루틴 실행
                    self.compass = GPS_V_2_0.GPS_HAT()  # GPS 관련 함수 선언
                    lat, long = self.compass.main() # GPS 데이터 얻기
                    print('위도:{}, 경도:{}'.format(lat, long))
                    publish.single(self.GPS_topics, str(self.StationID)+','+long+','+lat, hostname=self.broker, keepalive= 0)   # MQTT Server로 데이터 넣기
                    time.sleep(7) # int(self.StationID))   # 장비 별 데이터 넣는 시간 제어
            except Exception as e:
                print('Core2 error:',e)    # 에러 발생 시 에러를 표시하고 다시 원 코드로 돌아간다.
                #self.a += 1; self.b += 1
                #print("성공 횟수:{}, 실패 횟수:{}".format(self.a,self.b))
    def core3(self):
        while True:
            try:
                if not self.RxData.empty(): # 큐 버퍼가 차있으면 실행
                    Rx_data = self.RxData.get()
                    time.sleep(int(self.StationID)*3)
                    print('Core 3 Start')
                    publish.single(topic=self.data_topics, payload = Rx_data, hostname=self.broker,keepalive= 0)  # MQTT Server로 데이터 넣기                  
            except Exception as e:
                print('Core3 error:',e)    # 에러 발생 시 에러를 표시하고 다시 원 코드로 돌아간다.
    

 
        


if __name__ == "__main__":  # Main 함수 실행 루틴
    A = TM_Repeater()    # TM Repater

    while True:
        if A.NTP_SYNC():
            A.TRX_Controller_Switch(1)
            time.sleep(2)
            A.TRX_Controller_Switch(0)
            State, Station_ID = A.FPGA_Version_info()
            print('Station_ID: ', Station_ID)
            print('FPGA_Version Check Complited') 
            break
    while True:
        p1 = Process(target = A.core1, args = ())
        p2 = Process(target = A.core2, args = ())
        p3 = Process(target = A.core3, args = ())
        p1.start()
        p2.start()
        p3.start()
        p1.join()
        p2.join()
        p3.join()
        
