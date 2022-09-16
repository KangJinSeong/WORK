import socket
import time

conn = ('30.0.1.176',9000)
svr = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
svr.connect(conn)

ETH_start = time.time()
p = 0
# while p < 10:
#     p += 1
for i in range(9260):
    svr.send('{:3f}\n'.format(1).encode())

svr.close()    
ETH_end = time.time()

print(ETH_end-ETH_start)