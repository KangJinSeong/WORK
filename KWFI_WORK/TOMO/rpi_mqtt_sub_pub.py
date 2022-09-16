'''
Date: 2022.06.23
Title: 
By: Kang Jin Seong
'''
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

LED = 18    # GPIO 18에 LED 연결
SWITCH = 23 #GPIO 23에 스위치 연결
broker = "test.mosquitto.org"   #브로커 주소

def RPi_Set():  #GPIO 설정
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED,GPIO.OUT)
    GPIO.setup(SWITCH,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
    GPIO.output(LED, GPIO.LOW)  # 처음에는 LED OFF
    GPIO.setwarnings(False)

#브로커와 연결되면 실행되는 콜백 함수

def On_Connect(client, userdata, flags, rc):
    print("Connected with result code" + str(rc))
    client.subscribe("RPi/LED")

#메시지를 수신하면 실행되는 콜백 함수
def On_Message(client, userdata, msg):
    cmd = msg.payload.decode()
    print(msg.topic + "" + cmd)
    if cmd == "ON":   #LED ON
        GPIO.output(LED, GPIO.HIGH)
    elif cmd == "OFF":
        GPIO.output(LED, GPIO.LOW)
    else:
        print("INvalid message")
RPi_Set()
client = mqtt.Client()  #클라이언트 객체 생성
client.on_connect = On_Connect  #연결 콜백 함수 지정
client.on_message = On_Message  #메시지 수신 콜백 함수 시정

client.connect(broker, 1883, 60)    #브로커 연결
client.loop_start() #이벤트 루프 시작

while True:
    state = GPIO.input(SWITCH)  #스위치 상태 읽기
    if state == 1: #스위치 ON
        s_msg = "ON"
    else:
        s_msg = "OFF"

    client.publish("RPi/SWITCH", s_msg) #스위치 상태 메시지 발행
    time.sleep(2)   #2초 지연
