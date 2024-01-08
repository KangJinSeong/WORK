'''
Date: 2024.01.04
Title:  Mqtt_Subscribe_Publish Test_Code
By: Kang Jin Seong
'''
#publish_single()함수를 사용한 단일 메시지 발행 프로그램

import paho.mqtt.publish as publish
import time 
topics = 'Core/topic1'
topics2 = 'Core/topic2'
payload = "Hello Everyone"  #발행 메시지
broker = "test.mosquitto.org"   #브로커 주소

answer = ['DSPEN', 'TRXEN', 'TRXCSEM', 'MINTIN', 'BDTEMP', 'ENVTEMP', 'PRESSURE']
result = ','.join(answer)

while True:
    time.sleep(3)
    publish.single('Core/topic2', result, hostname = broker)   #메시지 발행
    publish.single('Core/topic3', payload, hostname = broker)   #메시지 발행
    publish.single('Core/topic4', 'HEKEKEKEK', hostname = broker)   #메시지 발행

    print("Message Published")