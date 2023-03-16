'''
Date: 2023.03.16
Title: 3차원해수유동 시간의 따른 TM_REPEATER SW REV(3)
By: Kang Jin seong
'''

from Subpy import GPS_V_1_0, TRX_Controller_Swtich, TRX_Triger #하드웨어 조작 관련 모듈
import RPi.GPIO as GPIO
import serial
from multiprocessing import Process, Queue
import paho.mqtt.subscribe as subcribe
import paho.mqtt.publish as publish
import time

class TM_Reapter:
    def __init__(self):
        self.Triger = TRX_Triger.TRX_TRG()
        self.compas = GPS_V_1_0.GPS_HAT()
        self.switch = TRX_Controller_Swtich.TRX_Power_switch()
        self.TIMEDATA = Queue()

        self.test_topics = 'Core/test12343Demension/data'
        self.broker ='test.mosquitto.org'

    def core1(self):    # FPGA Triger 신호 생성 함수
        while True:
            if not self.TIMEDATA.empty():    #큐버퍼가 차있으면 실행
                time_data = self.TIMEDATA.get()
                answer = self.Triger.Data_analysis(time_data)
                print(answer)
                if sum(answer) < 100:
                    self.Triger.timezone(hour=answer[0],min=answer[1],interval=answer[2],id=answer[3])
                    self.Triger.main()  # Main 코드 완성해야함

    def core2(self):
        try:
            while True:       
                m = subcribe.simple(self.test_topics, hostname=self.broker,keepalive = 0)
                print(m.payload.decode())
                self.TIMEDATA.put(m.payload.decode())
        except Exception as e:
            pass

    def core3(self):
        pass

    def core4(self):
        pass    

if __name__ == "__main__":
    
    A = TM_Reapter()
    print('Detecting')

    p1 = Process(target = A.core1, args=() )
    p2 = Process(target = A.core2, args=() )
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    