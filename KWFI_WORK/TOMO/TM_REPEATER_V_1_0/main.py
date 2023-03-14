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

        self.test_topics = 'Core/ttt'
        self.broker ='test.mosquitto.org'

    def core1(self):    # FPGA Triger 신호 생성 함수
        while True:
            if not self.TIMEDATA.empty():    #큐버퍼가 차있으면 실행
                time_data = self.TIMEDATA.get()
                td = time_data.split(',')
                self.Triger.timezone(hour=int(td[0]),min=int(td[1]),interval=int(td[2]),id=int(td[3]))
            self.Triger.main()  # Main 코드 완성해야함

    def core2(self):
        try:
            while True:       
                m = subcribe.simple(self.test_topics, hostname=self.broker,keepalive = 0)
                print(m.payload)
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
    