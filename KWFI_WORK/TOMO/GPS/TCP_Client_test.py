
from socket import *
from select import *

socks = [] # 소켓 목록
sock = socket()
server_ip = '30.0.1.59'

sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
socks.append(sock)	#생성된 소켓을 목록에 추가
sock.connect((server_ip, 2500))	#서버 연결

while True:
	r_sock, w_sock, e_sock = select(socks, [], [])	# 넌블록킹 모드
	if r_sock: #읽기 가능 이벤트 발생
		for s in r_sock:
			if s == sock:	#자신에게 온 데이터 인가?
				msg = sock.recv(1024).decode()
				print('수신 메세지:', msg)
	smsg = 'Done'
	sock.send(smsg.encode())
