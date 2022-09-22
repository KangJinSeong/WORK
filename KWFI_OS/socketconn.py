import socket
import threading
import time
import random

class socketServer:
    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.connSocket()

    def connSocket(self):
        #Socket 연결
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        # 포트 사용 중 에러 해결
        self.sock.bind((self.host,self.port))

        self.sock.listen(5)
        print("Waiting for incoming connections...")

        while True:
            # self.sock.settimeout(5)#타임아웃세팅
            self.conn,self.addr = self.sock.accept()
            self.conn.setblocking(True)
            self.mp = threading.Thread(target=self.receiveData,args=(self.conn,self.addr))
            self.mp.daemon = True
            self.mp.start()
    
    def receiveData(self,conn,addr):
        # 데이터 송수신
        try:
            while True:
                start = time.time()
                data = conn.recv(1024).decode()
                if not data:
                    # 데이터가 없을 때
                    break
                time.sleep(float(data))
                conn.send('{}'.format(random.randint(0,1)).encode())
                end = time.time()
                print(addr[0],addr[1])
                # print(end-start)
        except Exception as e:
            print("{}의 연결이 끊겼습니다.".format(addr[0]))
            socketServer(self.host,self.port)


if __name__ == '__main__':
    socketServer('',555)
    # '' == inaddr_any