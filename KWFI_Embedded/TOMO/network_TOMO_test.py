from datetime import datetime
import socket
import struct
import time


conn = ('30.0.1.16', 9000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind(conn)

server_socket.listen()

client_socket,addr = server_socket.accept()
print('Connected by', addr)
temp = b''
while True:
#     data = client_socket.recv(1024)


#     result = []
#     A = datetime.now()
#     result.append(A.year)
#     result.append(A.month)
#     result.append(A.day)
#     result.append(A.hour)
#     result.append(A.minute)
#     result.append(A.second)
#     print(result)
#     buf = struct.pack('%si' %len(result), *result)

    buf = '8000'.encode()
    client_socket.sendall(buf)

    time.sleep(1)
    
server_socket.close()
client_socket.close()

