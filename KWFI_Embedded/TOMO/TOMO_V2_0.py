'''
Date: 2022.09.15
Title: 3차원 해수유동 시스템 데이터 관리
By: Kang Jin Seong

'''

import RPi.GPIO as GPIO
import datetime as dt
import time
import serial

from multiprocessing import Process, Queue
import paho.mqtt.subscribe as subscribe


channel = 23    # 1pps 신호 입력 포트 설정
led = 18    # 트리거 신호 출력 포트 설정

GPIO.setmode(GPIO.BCM)  #GPIO 포트 설정은 
GPIO.setup(channel, GPIO.IN)    # 1pps 신호 입력 포트
GPIO.setup(led, GPIO.OUT)   # FPGA 트리거 출력 신호
GPIO.setwarnings(False)


state = 0   # 상태의 따른 트리거 제어 변수

def my_callback(channel):   # 1pps 라이징 에지 일때마다 인터럽트 걸려서 루트 처리
    global state
    print('GPS ON')
    if state == 1:
        GPIO.output(led, True)
        time.sleep(0.5)
        GPIO.output(led, False)
        state =0

GPIO.add_event_detect(channel, GPIO.RISING, callback = my_callback)

'''
triger(): 1pps 라이징 에지 신호에 맞춰 트리커 신호 출력
'''
def triger(serverRXdata):   # Core1:
    stopflag = False
    startflag = False
    start_m = 100
    starttime = False
    ptm = dt.datetime.now().minute
    while True:
        if not serverRXdata.empty(): # 큐버퍼가 꽉차있으면 실행
            maindata = serverRXdata.get()
            maindata = maindata.split(',')
            if maindata[0] == 'STOP':
                stopflag = True
                startflag = False
                starttime = False
                
            if maindata[len(maindata)- 1] == 'START':
                startflag = True
                start_m = maindata[len(maindata) - 3]              

        
        if stopflag:
            print('STOP')
            cm = dt.datetime.now().minute
            if dt.datetime.now().minute == int(start_m):
                starttime = True
                stopflag = False


        if startflag & starttime:
            print('Start')
            global state                    
            ctm = dt.datetime.now().minute
            print(ptm, ctm)

            if ctm >= ptm + int(maindata[len(maindata) - 2]):
                state = 1
                print(dt.datetime.now(), 'start')
                ptm = ctm
            if (60 == ptm + int(maindata[len(maindata) - 2])) & (ctm == 0):
                state = 1
                print(dt.datetime.now(), 'Start')
                ptm = ctm
            time.sleep(1)
        time.sleep(1)

    

def mqtt_subscribe_rasp(serverRXdata):
    topics = "Core/test12343Demension/data"
    broker = "test.mosquitto.org"

    while True:
        print('end')
        m = subscribe.simple(topics, hostname = broker,retained = False, msg_count = 1)
        print('Message:', m.payload)
        data = m.payload.decode('utf-8')
        serverRXdata.put(data)



def mqtt_publish_rasp(uartdata):
    topicRx = "Core/sendTestData1234/data"
    broker = "test.mosquitto.org"
    while True:
        if not uartdata.empty(): # 큐버퍼가 꽉차있으면 실행
            m = uartdata.get()
            print('Message:', m)
def uart_FPGA(uartdata):
    # serialIP = serial.Serial('/dev/ttyS0', baudrate= 9600, timeout = 10)
    serialIP = serial.Serial('/dev/ttyUSB0', baudrate= 9600, timeout = 10)
    while True:
        serialIP.write(b'\x3E\x35\x40\x30\x0D')
        data = serialIP.read(1024)
        print('RX data:',data)
        uartdata.put(data)
        

    


if __name__ == '__main__':
    serverRXdata = Queue()
    serverTXdata = Queue()
    uartdata = Queue()
    p1 = Process(target = triger, args =(serverRXdata,))
    p2 = Process(target = mqtt_subscribe_rasp, args = (serverRXdata,))
    p3 = Process(target = mqtt_publish_rasp, args = (uartdata,))
    p4 = Process(target = uart_FPGA, args = (uartdata, ))
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
