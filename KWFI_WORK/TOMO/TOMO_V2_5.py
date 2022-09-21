'''
Date: 2022.09.16
Title: 3차원 해수유동 시스템 데이터 관리
By: Kang Jin Seong

'''

import RPi.GPIO as GPIO
import datetime as dt
import time
import serial

from multiprocessing import Process, Queue
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import threading

import urllib
from urllib import request

channel = 23    # 1pps 신호 입력 포트 설정
led = 18    # 트리거 신호 출력 포트 설정

GPIO.setmode(GPIO.BCM)  #GPIO 포트 설정은 
GPIO.setup(channel, GPIO.IN)    # 1pps 신호 입력 포트
GPIO.setup(led, GPIO.OUT)   # FPGA 트리거 출력 신호
GPIO.setwarnings(False)


state = 0   # 상태의 따른 트리거 제어 변수

def my_callback(channel):   # 1pps 라이징 에지 일때마다 인터럽트 걸려서 루트 처리
    global state
    # ~ s = statedata.get() 
    # ~ print('GPS ON')
    
    if state == 1:
        time.sleep(0.2)
        GPIO.output(led, True)
        time.sleep(3)
        GPIO.output(led, False)
        state = 0

    


'''
triger(): 1pps 라이징 에지 신호에 맞춰 트리커 신호 출력
'''
def triger(serverRXdata, statedata):   # Core1:
    stopflag = False
    startflag = False
    start_m = 100
    starttime = False
    global state 
    
    # ~ GPIO.add_event_detect(channel, GPIO.RISING, callback = my_callback)
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
            # ~ print('STOP')
            cm = dt.datetime.now().minute
            if dt.datetime.now().minute == int(start_m):
                starttime = True
                stopflag = False
                ptm = dt.datetime.now().minute   


        if startflag & starttime:
            # ~ print('Start')                   
            ctm = dt.datetime.now().minute
            # ~ print(ptm, ctm)

            if ctm >= ptm + int(maindata[len(maindata) - 2]):
                state = 1
                time.sleep(0.2)
                GPIO.output(led, True)
                time.sleep(3)
                GPIO.output(led, False)
                # ~ statedata.put(state)
                print(dt.datetime.now(), 'start')
                ptm = ctm
            if (60 == ptm + int(maindata[len(maindata) - 2])) & (ctm == 0):
                state = 1
                time.sleep(0.2)
                GPIO.output(led, True)
                time.sleep(3)
                GPIO.output(led, False)                
                # ~ statedata.put(state)
                print(dt.datetime.now(), 'Start')
                ptm = ctm

            # ~ time.sleep(1)
        # ~ time.sleep(1)

    

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
    topics = "Core/sendTestData1234/data"
    topics1 = "Core/test12343Demension/version"
    broker = "test.mosquitto.org"

    while True:
        if not uartdata.empty(): # 큐버퍼가 꽉차있으면 실행

            m = uartdata.get()
            print(m)
            publish.single(topics, m , hostname = broker)
            print('Done')
        # ~ print(GPIO.input(channel))
        if GPIO.input(channel) == 1:
            print('GPS ON')
            publish.single(topics1, 'GPS2', hostname = broker)

        time.sleep(0.7)


def uart_FPGA(uartdata):
    serialIP = serial.Serial('/dev/ttyS0', baudrate= 115200)

    while True:
        dat = serialIP.readline()
        print("RX DATA:", dat)
        dat = dat.decode()
        if dat[0] == '(':
            dat = dat[:len(dat)-2]
            dat = dat.replace(")(", ",")
            dat = '2' + dat
            uartdata.put(dat)
        
    
def version_on():
    topics = "Core/test12343Demension/version"
    broker = "test.mosquitto.org"   
    serialIP = serial.Serial('/dev/ttyS0', baudrate= 115200, timeout = 10)
    while True:
        serialIP.write(b'>5@0\r')
        data = serialIP.read(1024)
        print(data)
        if data.decode()[:4] == '>5@0':
            publish.single(topics,'FV2ON', hostname = broker) 
            return True
            break
        else:
            publish.single(topics,'FV2OFF', hostname = broker) 
            return False

def internet_on():
    try:
        request.urlopen('http://223.130.200.107', timeout = 1)
        return True
    except urllib.error.URLError as err:
        return False


if __name__ == '__main__':
    serverRXdata = Queue()
    serverTXdata = Queue()
    uartdata = Queue()
    statedata = Queue()
    while True:
        print('version Detect')
        time.sleep(3)
        if version_on() & internet_on():
            print('Done')
            p1 = Process(target = triger, args =(serverRXdata, statedata,))
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
            
            break
