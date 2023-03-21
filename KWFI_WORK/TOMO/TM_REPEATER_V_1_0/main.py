'''
Date: 2023.03.16
Title: 3차원해수유동 시간의 따른 TM_REPEATER SW REV(3)
By: Kang Jin seong
'''

from Subpy import TRX_Controller_Swtich, TRX_Triger, GPS_V_1_0 #하드웨어 조작 관련 모듈
from Subpy import UART_V_1_0
import RPi.GPIO as GPIO
import serial
from multiprocessing import Process, Queue
import paho.mqtt.subscribe as subcribe
import paho.mqtt.publish as publish
import time

class TM_Reapter:
    def __init__(self):
        self.Triger = TRX_Triger.TRX_TRG()
        self.UARTIP = UART_V_1_0.UART_HAT()
        self.compass = GPS_V_1_0.GPS_HAT()

        self.TIMEDATA = Queue()

        self.data_topics = 'Core/test12343Demension/data'
        self.GPS_topics = 'Core/test12343Demension/version'

        self.broker ='test.mosquitto.org'



        self.StationID = 0

        self.startflag = 0

    def core1(self):    # FPGA Triger 신호 생성 함수
        try:
            while True:
                if not self.TIMEDATA.empty():    #큐버퍼가 차있으면 실행           
                    time_data = self.TIMEDATA.get()
                    answer = self.Triger.Data_analysis(time_data)
                    print('Time Data SEt:',answer)
                    if sum(answer) != 0:
                        self.startflag = 1
                        self.Triger.timezone(hour=answer[0],min=answer[1],interval=answer[2],id=answer[3])
                    else:
                        self. startflag = 0
                if self.startflag:
                    self.Triger.main(self.StationID)
        
                # Publish(sigdata, bddata 등)
        except Exception as e:
            print(e)
            pass

    def core2(self):
        try:
            while True:       
                m = subcribe.simple(self.data_topics, hostname=self.broker, keepalive=0)
                print('MQTT Subcribe:',m.payload.decode())
                self.TIMEDATA.put(m.payload.decode())
        except Exception as e:
            print(e)
            pass

    def core3(self):
        try:
            while True:
                if self.StationID != 0: 
                    lat, long = self.compass.main()
                    print('위도:{}, 경도:{}'.format(lat, long))
                    publish.single(self.GPS_topics, str(self.StationID)+','+long+','+lat, hostname=self.broker, keepalive=0)
                    time.sleep(7)
        except Exception as e:
            print(e)
            pass

    def core4(self):
        pass
    def FPGA_Version_info(self):
        data = self.UARTIP.FPGA_Dat_analysis()
        print(data)
        if 'Correlator_ID' in data:
            answer = data.split('=')
            self.StationID = answer[1][1]
            State = 1
        else:
            self.StationID = 0
            State = 0
         
        
        return State, self.StationID   

if __name__ == "__main__":
    
    B = TRX_Controller_Swtich.TRX_Power_switch()
    B.main(0)
    time.sleep(2)
    B.main(1)
    A = TM_Reapter()

    while True:
        State, Station_ID = A.FPGA_Version_info()
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