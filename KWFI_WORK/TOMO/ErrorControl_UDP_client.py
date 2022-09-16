'''
Date: 2022.06.10
Title:
By: Kang Jin Seong
'''
import random
from socket import *

port = 2500
BUFFER = 1024
server = '30.0.1.31'
c_sock = socket(AF_INET, SOCK_DGRAM)
c_sock.connect((server,port))	# 일반적으로 연결 없이 전송을 하지만 connect()함수를 이용하여 상대방과 먼저 연결하면 send(), recv() 함수를 이용할 수 있다.

for i in range(10):	# 10번시도
	delay = 0.1
	data = "Hello message"
	
	while True:
		c_sock.send(data.encode())
		print(f"Waiting up to {delay} seconds for a reply")
		c_sock.settimeout(delay)	# 타임아웃 설정
		try:
			data = c_sock.recv(BUFFER)	#데이터 수신
		except timeout:
			delay *= 2	#대기시간 2배 증가
			if delay > 2.0:	# 시간 초과
				print("The sever seems to be down")
				break
		else:
			print('Response:', data.decode())
			break	# 종료
			
		
