'''
Date: 2022.06.22
Title: 
By: Kang Jin Seong
'''
#간단한 mqtt 메시지 구독 프로그램

import paho.mqtt.subscribe as subscribe

topics = 'mqtt/test'
# ~ topics = 'control/LED'
broker = "test.mosquitto.org"
m = subscribe.simple(topics, hostname= broker, retained= False,msg_count= 1)
print('Topics:', m.topic)
print('Message:', m.payload.decode())   #메시지
