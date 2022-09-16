# import socketconn

# socketconn.socketServer('',555)
# # '' == inaddr_any

import socket
import time

conn = ('30.0.1.163',8080)

svr = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
svr.connect(conn)
start = time.time()

while True:

    svr.send(str(0.01).encode())
    data = svr.recv(1024).decode()
    print(data)

end = time.time()
print(end-start)
svr.close()