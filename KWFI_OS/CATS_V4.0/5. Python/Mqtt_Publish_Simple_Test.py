'''
Date: 2024.01.08
Title:  Mqtt_Subscribe_Publish Test_Code
By: Kang Jin Seong
'''
#publish_single()함수를 사용한 단일 메시지 발행 프로그램

with open("2_4.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

# 각 줄에서 줄바꿈 문자 제거
lines = [line.strip() for line in lines]
result = ','.join(lines)

A_1_2 = '(1,2,237312,'+ result +',)'
A_1_3 = '(1,3,237312,'+ result +',)'
A_1_4 = '(1,4,237312,'+ result +',)'
A_1_5 = '(1,5,237312,'+ result +',)'

A_2_1 = '(2,1,237312,'+ result +',)'
A_2_3 = '(2,3,237312,'+ result +',)'
A_2_4 = '(2,4,237312,'+ result +',)'
A_2_5 = '(2,5,237312,'+ result +',)'

A_3_1 = '(3,1,237312,'+ result +',)'
A_3_2 = '(3,2,237312,'+ result +',)'
A_3_4 = '(3,4,237312,'+ result +',)'
A_3_5 = '(3,5,237312,'+ result +',)'

with open("4_2.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

# 각 줄에서 줄바꿈 문자 제거
lines = [line.strip() for line in lines]
result = ','.join(lines)

A_4_1 = '(4,1,237363,'+ result +',)'
A_4_2 = '(4,2,237363,'+ result +',)'
A_4_3 = '(4,3,237363,'+ result +',)'
A_4_5 = '(4,5,237363,'+ result +',)'

A_5_1 = '(5,1,237363,'+ result +',)'
A_5_2 = '(5,2,237363,'+ result +',)'
A_5_3 = '(5,3,237363,'+ result +',)'
A_5_4 = '(5,4,237363,'+ result +',)'

b = [A_1_2, A_1_3, A_1_4, A_1_5, A_2_1, A_2_3, A_2_4, A_2_5, A_3_1, A_3_2, A_3_4, A_3_5, A_4_1, A_4_2, A_4_3, A_4_5, A_5_1, A_5_2, A_5_3, A_5_4]

import paho.mqtt.publish as publish
import time
from multiprocessing import Process
topics = 'Core/topic1'
topics2 = 'KWFI/3D/BDDATA/Update'

broker = "test.mosquitto.org"   #브로커 주소

answer_1 = ['12.35', 'NONE', '22.5', '3.5','+0.12', '-0.01','24.5','1']
answer_2 = ['12.31', 'NONE', '22.5', '4.7','+0.34', '-0.2','25.5','2']
answer_3 = ['12.48', 'NONE', '22.1', '3.3','+0.21', '-0.35','22.5','3']
answer_4 = ['12.74', 'NONE', '22.2', '5.6','+0.01', '+0.02','26.5','4']
answer_5 = ['12.45', 'NONE', '22.6', '6.5','+0.29', '-0.4','21.5','5']

result_1 = ','.join(answer_1)
result_2 = ','.join(answer_2)
result_3 = ','.join(answer_3)
result_4 = ','.join(answer_4)
result_5 = ','.join(answer_5)

answer_a_1 = ['1PPS', '34.83987667', '127.7747667', '1']
answer_a_2 = ['1PPS', '34.84847667', '127.77549500', '2']
answer_a_3 = ['1PPS', '34.8470034', '127.81188359', '3']
answer_a_4 = ['1PPS', '34.83138833', '127.81453167', '4']
answer_a_5 = ['1PPS', '34.8384671', '127.8125', '5']

result_a_1 = ','.join(answer_a_1)
result_a_2 = ','.join(answer_a_2)
result_a_3 = ','.join(answer_a_3)
result_a_4 = ','.join(answer_a_4)
result_a_5 = ','.join(answer_a_5)


while True:
    try:

        a = f'queue2:{result_2}, queue3:{b[0]}, queue4:{result_a_2}'
        publish.single(topics2, a,hostname=broker)   #메시지 발행
        print('BDDATA Published')
        print(f'SIGDATA Publisskehhed')
        time.sleep(3)

        a = f'queue2:{result_3}, queue3:{b[1]}, queue4:{result_a_3}'
        publish.single(topics2, a,hostname=broker)   #메시지 발행
        print('BDDATA Published')
        print(f'SIGDATA Publisskehhed')
        time.sleep(3)

        a = f'queue2:{result_4}, queue3:{b[2]}, queue4:{result_a_4}'
        publish.single(topics2, a,hostname=broker)   #메시지 발행
        print('BDDATA Published')
        print(f'SIGDATA Publisskehhed')
        time.sleep(3)

        a = f'queue2:{result_5}, queue3:{b[3]}, queue4:{result_a_5}'
        publish.single(topics2, a,hostname=broker)   #메시지 발행
        print('BDDATA Published')
        print(f'SIGDATA Publisskehhed')
        time.sleep(3)

        a = f'queue2:{result_1}, queue3:{b[4]}, queue4:{result_a_1}'
        publish.single(topics2, a,hostname=broker)   #메시지 발행
        print('BDDATA Published')
        print(f'SIGDATA Publisskehhed')
        time.sleep(3)

        a = f'queue2:{result_3}, queue3:{b[5]}, queue4:{result_a_3}'
        publish.single(topics2, a,hostname=broker)   #메시지 발행
        print('BDDATA Published')
        print(f'SIGDATA Publisskehhed')
        time.sleep(3)

        a = f'queue2:{result_4}, queue3:{b[6]}, queue4:{result_a_4}'
        publish.single(topics2, a,hostname=broker)   #메시지 발행
        print('BDDATA Published')
        print(f'SIGDATA Publisskehhed')
        time.sleep(3)

        a = f'queue2:{result_5}, queue3:{b[7]}, queue4:{result_a_5}'
        publish.single(topics2, a,hostname=broker)   #메시지 발행
        print('BDDATA Published')
        print(f'SIGDATA Publisskehhed')
        time.sleep(3)

        a = f'queue2:{result_1}, queue3:{b[8]}, queue4:{result_a_1}'
        publish.single(topics2, a,hostname=broker)   #메시지 발행
        print('BDDATA Published')
        print(f'SIGDATA Publisskehhed')
        time.sleep(3)

        a = f'queue2:{result_2}, queue3:{b[9]}, queue4:{result_a_2}'
        publish.single(topics2, a,hostname=broker)   #메시지 발행
        print('BDDATA Published')
        print(f'SIGDATA Publisskehhed')
        time.sleep(3)

        a = f'queue2:{result_4}, queue3:{b[10]}, queue4:{result_a_4}'
        publish.single(topics2, a,hostname=broker)   #메시지 발행
        print('BDDATA Published')
        print(f'SIGDATA Publisskehhed')
        time.sleep(3)

        a = f'queue2:{result_5}, queue3:{b[11]}, queue4:{result_a_5}'
        publish.single(topics2, a,hostname=broker)   #메시지 발행
        print('BDDATA Published')
        print(f'SIGDATA Publisskehhed')
        time.sleep(3)

        a = f'queue2:{result_1}, queue3:{b[12]}, queue4:{result_a_1}'
        publish.single(topics2, a,hostname=broker)   #메시지 발행
        print('BDDATA Published')
        print(f'SIGDATA Publisskehhed')
        time.sleep(3)

        a = f'queue2:{result_2}, queue3:{b[13]}, queue4:{result_a_2}'
        publish.single(topics2, a,hostname=broker)   #메시지 발행
        print('BDDATA Published')
        print(f'SIGDATA Publisskehhed')
        time.sleep(3)

        a = f'queue2:{result_3}, queue3:{b[14]}, queue4:{result_a_3}'
        publish.single(topics2, a,hostname=broker)   #메시지 발행
        print('BDDATA Published')
        print(f'SIGDATA Publisskehhed')
        time.sleep(3)

        a = f'queue2:{result_5}, queue3:{b[15]}, queue4:{result_a_5}'
        publish.single(topics2, a,hostname=broker)   #메시지 발행
        print('BDDATA Published')
        print(f'SIGDATA Publisskehhed')
        time.sleep(3)

        a = f'queue2:{result_1}, queue3:{b[16]}, queue4:{result_a_1}'
        publish.single(topics2, a,hostname=broker)   #메시지 발행
        print('BDDATA Published')
        print(f'SIGDATA Publisskehhed')
        time.sleep(3)

        a = f'queue2:{result_2}, queue3:{b[17]}, queue4:{result_a_2}'
        publish.single(topics2, a,hostname=broker)   #메시지 발행
        print('BDDATA Published')
        print(f'SIGDATA Publisskehhed')
        time.sleep(3)

        a = f'queue2:{result_3}, queue3:{b[18]}, queue4:{result_a_3}'
        publish.single(topics2, a,hostname=broker)   #메시지 발행
        print('BDDATA Published')
        print(f'SIGDATA Publisskehhed')
        time.sleep(3)

        a = f'queue2:{result_4}, queue3:{b[19]}, queue4:{result_a_4}'
        publish.single(topics2, a,hostname=broker)   #메시지 발행
        print('BDDATA Published')
        print(f'SIGDATA Publisskehhed')
        time.sleep(3)

    except:
        pass