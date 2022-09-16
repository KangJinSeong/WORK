'''
Date: 2022.06.09
Title:
By: Kang Jin Seong
'''

#TCP 에코 서버
# 1명의 클라이언트만 서비스 한다.

from socket import *

port = 2500
BUFSIZE = 1024

sock = socket(AF_INET, SOCK_STREAM)
sock.bind(('',port))	#자신의 주소 사용
sock.listen(1)	# 최대 대기 클라이언트 수
print('Waiting for Clients...')

# 클라이언트의 연결 요청을 받는다.
c_sock, (r_host, r_port) = sock.accept()
print('Connected by', r_host, r_port)

while True:
	#상대방 메세지 수신
	data = c_sock.recv(BUFSIZE)
	if not data:	# 연결이 종료 되었으면 빈문자 수신
		c_sock.close()
		print('연결이 종료되었습니다.')
	print("Received message:", data.decode())
	c_sock.send(data)
c_sock.close()
