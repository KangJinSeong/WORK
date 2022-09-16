'''
Date: 2022.06.22
Title: 
By: Kang Jin Seong
'''

#GPIO23에 연결된 스위치 상태를 읽어 메시지를 발행하는 프로그램

import paho.mqtt.publish as publish
import RPi.GPIO as GPIO
import time

topic = "RPi/SWITCH-1"
broker = "test.mosquitto.org"

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)   #GPIO23 = 입력모드
# ~ GPIO.setup(23, GPIO.IN)
print("Checking Switch on GPIO23")
while True:
    led_state = GPIO.input(23)  # 스위치 상태 읽기
    if led_state == 1:
        msg = "Switch ON"
    else:
        msg = "Switch OFF"

    #스위치 상태 발행
    publish.single(topic, msg, hostname=broker)
    time.sleep(1)   #1초후 다시 전송
