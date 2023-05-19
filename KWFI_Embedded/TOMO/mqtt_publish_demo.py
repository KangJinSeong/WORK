'''
Date: 2022.06.22
Title: 
By: Kang Jin Seong
'''
# 두개의 토픽에 대해 각각 하나씩의 메시지를 발행하는 프로그램

import paho.mqtt.publish as publish

# MQTT 브로커: test.mosquitto.org, iot.eclipse.org
broker = "test.mosquitto.org"
publish.single("Core/topic1", "Hello", hostname= broker)
publish.single("Core/topic2", "World!", hostname= broker)

print("Done")