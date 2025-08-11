'''
Date: 2024.01.30
Title:  Mqtt_Publish_Client Code(Simple로 변경)
By: Kang Jin Seong
'''

import paho.mqtt.publish as publish
topics = 'Core/topic1'
broker = "test.mosquitto.org"

def Mqtt_Publish(order,Q):
    try:
        answer = f"Stop,{order},{Q},Start"
        publish.single(topics,answer,hostname=broker)   #메시지 발행
        return f"DAta Published"
    except:
        pass
def Mqtt_Publish_2():
    try:
        answer = f"WAKE"
        publish.single(topics,answer,hostname=broker)   #메시지 발행
        return f"DAta Published"
    except:
        pass