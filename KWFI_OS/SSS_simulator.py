
'''
Date: 2022.08.24
Title: 사이드스캔 소나 시뮬레이터
By: Kang Jin Seong
'''

import struct
from socket import *
import time

''' --------------------------------------------------------------------------------------------'''

start_flag = '0x5A5A5A5A'
packet_length = 20
# msgID_1 = 1
# msgID_2 = 2
# value_index = 0
# value_data = 0
## NI 소켓통신 엔디안: 빅 엔디안
# convert_start_flag = int(start_flag, 16)
# pack_flag = struct.pack('>i', convert_start_flag)
# pack_length = struct.pack('>i', packet_length)

# pack_msgID_1 = struct.pack('>i', msgID_1)
# pack_msgID_2 = struct.pack('>i', msgID_2)

# pack_value_index = struct.pack('>i', value_index)
# pack_value_data = struct.pack('>i', value_data)

convert_start_flag = int(start_flag, 16)
pack_flag = struct.pack('>i', convert_start_flag)
pack_length = struct.pack('>i', packet_length)

pack_msgID_2 = struct.pack('>i', 2)
pack_msgID_3 = struct.pack('>i', 3)
pack_msgID_4 = struct.pack('>i', 4)
pack_msgID_5 = struct.pack('>i', 5)
pack_msgID_6 = struct.pack('>i', 6)
pack_msgID_7 = struct.pack('>i', 7)


pack_value_2_index = struct.pack('>i', 1)
pack_value_3_index = struct.pack('>i', 1)
pack_value_4_index = struct.pack('>i', 100)
pack_value_5_index = struct.pack('>i', 255)
pack_value_6_index = struct.pack('>i', 4)
pack_value_7_index = struct.pack('>i', 4)


pack_value_2_data = struct.pack('>i', 0)
pack_value_3_data = struct.pack('>i', 0)
pack_value_4_data = struct.pack('>i', 0)
pack_value_5_data = struct.pack('>i', 0)
pack_value_6_data = struct.pack('>i', 0)
pack_value_7_data = struct.pack('>i', 0)

bin_data_1 = pack_flag + pack_length + pack_msgID_3 + pack_value_3_index + pack_value_3_data
bin_data_2 = pack_flag + pack_length + pack_msgID_5 + pack_value_5_index + pack_value_5_data
bin_data_3 = pack_flag + pack_length + pack_msgID_6 + pack_value_6_index + pack_value_6_data
bin_data_4 = pack_flag + pack_length + pack_msgID_7 + pack_value_7_index + pack_value_7_data
bin_data_5 = pack_flag + pack_length + pack_msgID_4 + pack_value_4_index + pack_value_4_data
bin_data_6 = pack_flag + pack_length + pack_msgID_2 + pack_value_2_index + pack_value_2_data
# print(bin_data_1)
''' --------------------------------------------------------------------------------------------'''

port = 2500
BUFSIZE = 1024

sock = socket(AF_INET, SOCK_STREAM)
sock.bind(('', port))   # 자신의 주소 사용
sock.listen(1)  # 최대 대기 클라이언트 수
print('Waiting for clients...')

# 클라이언트의 연결 요청을 받는다.
c_sock, (r_host, r_port) = sock.accept()
print('Connected by', r_host, r_port)
time.sleep(1)
c_sock.send(bin_data_1)
c_sock.send(bin_data_2)
c_sock.send(bin_data_3)
c_sock.send(bin_data_4)
c_sock.send(bin_data_5)
c_sock.send(bin_data_6)
# time.sleep(10)
# c_sock.send(bin_data_1)
# c_sock.send(bin_data_2)
# c_sock.send(bin_data_3)
# c_sock.send(bin_data_4)
# c_sock.send(bin_data_5)
# c_sock.send(bin_data_6)
while True:
    print('end')
    time.sleep(1)
# time.sleep(1)
# 수신 메세지를 다시 전송

# while True: 
#     try:
#         # 수신 메세지를 다시 전송
#         c_sock.send(bin_data_1)
#         c_sock.send(bin_data_2)
#         c_sock.send(bin_data_3)
#         c_sock.send(bin_data_4)
#         c_sock.send(bin_data_5)
#         c_sock.send(bin_data_6)
#         print(bin_data_1)
#         print(bin_data_2)
#         print(bin_data_3)
#         print(bin_data_4)
#         print(bin_data_5)
#         print(bin_data_6)

#         time.sleep(1)

#     except:
#         print('연결이 종료되었습니다.')
#         c_sock.close()
#         break   #무한 루프 종료
# c_sock.close()
