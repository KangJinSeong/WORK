'''
Date: 2022.06.23
Title: 
By: Kang Jin Seong
'''

# mqtt를 이용하여 GPIO18에 연결된 LED를 제어하는 구독 프로그램(라즈베리파이)

import paho.mqtt.subscribe as subscribe
import RPi.GPIO as GPIO
import time

LED = 18    # GPIO 18에 LED 연결

def RPi_Set():  #GPIO 설정
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED,GPIO.OUT)
    GPIO.output(LED, GPIO.LOW)  # 처음에는 LED OFF
    GPIO.setwarnings(False)

topics = ['RPi/LED']
print('Topic:', topics[0])
RPi_Set()

while True:
    m = subscribe.simple(topics, hostname="test.mosquitto.org", retained=False)
    r_msg = m.payload.decode()   # 수신 메시지
    print(m.topic + "" + r_msg)

    if r_msg == "ON":   #LED ON
        GPIO.output(LED, GPIO.HIGH)
    elif r_msg == "OFF":
        GPIO.output(LED, GPIO.LOW)
    else:
        print("INvalid message")
    time.sleep(0.5)
