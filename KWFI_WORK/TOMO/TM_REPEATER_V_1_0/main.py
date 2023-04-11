'''
Date: 2023.03.29
Title: TM_REPEATER SW REV(7)
By: Kang Jin seong
'''

from Subpy import TRX_Controller_Swtich, TRX_Triger, GPS_V_1_0 #하드웨어 조작 관련 모듈
from Subpy import UART_V_1_0    #UART 통신 관련 모듈
from multiprocessing import Process, Queue  # 멀티 프로세싱 관련 모듈
import paho.mqtt.subscribe as subcribe  # MQTT 수신 관련 모듈
import paho.mqtt.publish as publish     # MQTT 송신 관련 모듈
import time     # 라즈베리파이 시간 관련 모듈

class TM_Repeater:
    def __init__(self):
        # ※ 클래스 함수 내부 모듈 선언
        self.Triger = TRX_Triger.TRX_TRG()  # FPGA 트리거 관련 함수 선언 
        self.UARTIP = UART_V_1_0.UART_HAT() # UART 통신 관련 함수 선언
        self.TIMEDATA = Queue() # Q 버퍼 선언
        # ※ MQTT 서버 관련 변수 선언
        self.data_topics = 'Core/test12343Demension/data'   # MQTT 제어신호 관련 토픽
        self.GPS_topics = 'Core/test12343Demension/version' # MQTT GPS 신호 관련 토픽
        self.broker ='test.mosquitto.org'   # MQTT 브로커
        # ※ 변수 선언
        self.StationID = 0  # 장비 시리얼 넘버
        self.startflag = 0  # 시작 신호 제어 상태 값
        self.a = 0
        self.b = 0
    def core1(self):    # Main Server로 부터 입력된 시간에 따라 TRX Controller를 구동하기 위한 Triger 신호 출력 함수
        while True:
            try:
                if not self.TIMEDATA.empty():    #큐버퍼가 차있으면 실행          
                    time_data = self.TIMEDATA.get() # 큐 데이터 얻기
                    answer = self.Triger.Data_analysis(time_data)   # 큐 데이터 분석
                    print('Time Data Set:',answer)
                    if sum(answer) != 0:    # 시작 명령어
                        self.startflag = 1
                        self.Triger.timezone(hour=answer[0],min=answer[1],interval=answer[2],id=answer[3])  # 시작 시간 설정
                    else:
                        self.startflag = 0
                        self.Triger.timezone(hour=answer[0],min=answer[1],interval=answer[2],id=answer[3])  # 시작 시간 설정
                if self.startflag:
                    self.Triger.main(self.StationID)  # TRX Controller 작동 루틴
            except Exception as e:
                print('Core1 error:',e)    # 에러 발생 시 에러를 표시하고 다시 원 코드로 돌아간다.
                self.a += 1; self.b += 1
                print("성공 횟수:{}, 실패 횟수:{}".format(self.a,self.b))
    def core2(self):
            while True:
                try:            
                    m = subcribe.simple(self.data_topics, hostname=self.broker, keepalive=20)   # MQTT Server로부터 데이터 얻기
                    time.sleep(3)
                    print('MQTT Subcribe:',m.payload.decode())
                    self.TIMEDATA.put(m.payload.decode())   # 큐 버퍼에 데이터 넣기
                except Exception as e:
                    print('Core2 error:',e)    # 에러 발생 시 에러를 표시하고 다시 원 코드로 돌아간다.
                    self.a += 1; self.b += 1
                    print("성공 횟수:{}, 실패 횟수:{}".format(self.a,self.b))
    def core3(self):
        while True:
            try:
                if self.StationID != 0:     # 장비 시리얼 넘버를 얻은 후 아래 루틴 실행
                    self.compass = GPS_V_1_0.GPS_HAT()  # GPS 관련 함수 선언
                    lat, long = self.compass.main() # GPS 데이터 얻기
                    print('위도:{}, 경도:{}'.format(lat, long))
                    publish.single(self.GPS_topics, str(self.StationID)+','+long+','+lat, hostname=self.broker, keepalive= 0)   # MQTT Server로 데이터 넣기
                    time.sleep(7) # int(self.StationID))   # 장비 별 데이터 넣는 시간 제어
            except Exception as e:
                print('Core3 error:',e)    # 에러 발생 시 에러를 표시하고 다시 원 코드로 돌아간다.
                self.a += 1; self.b += 1
                print("성공 횟수:{}, 실패 횟수:{}".format(self.a,self.b))               
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

if __name__ == "__main__":  # Main 함수 실행 루틴
    B = TRX_Controller_Swtich.TRX_Power_switch()    # Switch 보드 제어를 위한 함수 선언
    B.main(0)   # TRX Controller 전원 OFF
    time.sleep(2)   # 안정화 시간
    B.main(1)   # TRX Controller 전원 ON
    A = TM_Repeater()    # TM Repater
    while True:
        State, Station_ID = A.FPGA_Version_info()   # 장비별 시리얼 번호 얻기를 위한 함수
        if State:
            print('Station_Number:',Station_ID)
            print('FPGA_Version Check Complited') 
            p1 = Process(target = A.core1, args=() )
            p2 = Process(target = A.core2, args=() )
            p3 = Process(target = A.core3, args=() )
            p1.start()
            p2.start()
            p3.start()
            p1.join()
            p2.join()
            p3.join()
        else:
            print('FPGA_Version Unknown') 