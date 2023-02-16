'''
Date: 2023.02.15
Title: 3차원 해수우동 TRX_Controller 시뮬레이터 연습용 코드
By: Kang Jin Seong
'''

#TCP 에코 서버
# 1명의 클라이언트만 서비스 한다.

from socket import *
import struct
import matplotlib.pyplot as plt
import numpy as np

port = 2500
BUFSIZE = 1024

sock = socket(AF_INET, SOCK_STREAM)
sock.bind(('',port))	#자신의 주소 사용
sock.listen(1)	# 최대 대기 클라이언트 수
print('Waiting for Clients...')

# 클라이언트의 연결 요청을 받는다.
c_sock, (r_host, r_port) = sock.accept()
print('Connected by', r_host, r_port)
result = b''
while True:
	#상대방 메세지 수신
	data = c_sock.recv(BUFSIZE)
	if not data:	# 연결이 종료 되었으면 빈문자 수신
		c_sock.close()
		print('연결이 종료되었습니다.')
		break
	print("Received message:", data)
	result += data
c_sock.close()

un_data = np.frombuffer(result, dtype = '>f')
t = np.arange(start = 0, stop = len(un_data)) * (1/440000)
plt.figure()
plt.plot(t, un_data)
print(len(t), len(un_data))

plt.show()