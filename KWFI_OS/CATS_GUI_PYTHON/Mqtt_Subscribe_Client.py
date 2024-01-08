'''
Date: 2024.01.04
Title:  Mqtt_Subscribe_Client Code
By: Kang Jin Seong
'''
import paho.mqtt.client as mqtt
import time

#글로벌 변수 설정
queue2 = []  
queue3 = []
queue4 = []

def on_connect(client, userdata, flags, rc):
    '''
    서버와 연결이 되었을 때 실행 되는 콜 백 함수
    '''
    # print("Connected with result code"+ str(rc))
    '''
    1) 토픽과 연결이 될 때마다 새로 연결(구독)신청
    2) Topics2: BDDATA, Topics3: SIGDATA, Topics4: GPSDATA
    '''
    client.subscribe("Core/topic2")
    client.subscribe("Core/topic3")
    client.subscribe("Core/topic4")

def on_message(client, userdata, msg):
    '''
    메시지를 수신 했을 때 실행되는 콜백 함수
    queue: 토픽별로 메세지를 수신했을때 Labview와 데이터 전달을 위한 변수
        - queue2: BDDATA 변수
        - queue3: SIGDATA 변수
        - queue4: GPSDATA 변수
    '''
    # 함수내 변수 사용을 위한 글로벌 변수 사용
    global queue
    # print(msg.topic + "" + str(msg.payload))
    '''
    토픽별로 관련한 메세지 전달 블록
    '''
    if msg.topic == "Core/topic2":
        queue2.append(msg.payload.decode())
    elif msg.topic == "Core/topic3":
        queue3.append(msg.payload.decode())
    elif msg.topic == "Core/topic4":
        queue4.append(msg.payload.decode())   

def Mqtt_Subscribe():
    '''
    Mqtt 클라이언트 객체를 생성하고 콜백 함수 연결
    이벤트 루프 상에서 작동하여 Main Processor와 별개로 작동한다.
    '''
    global queue
    '''
    클라이언트 생성 및 콜백 함수 연결
    '''
    client = mqtt.Client() 
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect('test.mosquitto.org', 1883, 60)
    '''
    이벤트 루프 Main 루틴
    Labview 프로그램과 연동 루틴
    Time out: 7s(연동 시험을 통한 데이터 확정)
    '''
    client.loop_start()
    time.sleep(7)
    client.loop_stop()
    if queue2 != [] and queue3 != [] and queue4 != []:
        return f'queue2:{queue2[0]}, queue3:{queue3[0]}, queue4:{queue4[0]}'
    elif queue2 != [] and queue4 != []:
        return f'queue2:{queue2[0]}, queue4:{queue4[0]}'    
    elif queue3 != [] and queue4 != []:
        return f'queue3:{queue3[0]}, queue4:{queue4[0]}'
    elif queue2 != [] and queue3 != []:
        return f'queue2:{queue2[0]}, queue3:{queue3[0]}' 
    else:
        return 'None'    
