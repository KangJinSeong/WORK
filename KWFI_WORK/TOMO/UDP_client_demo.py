'''
Date: 2022.06.09
Title:
By: Kang Jin Seong
'''

import socket
BUFFSIZE = 1024
port = 2500


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
msg = "Hello UDP Server"
sock.sendto(msg.encode(), ('30.0.1.31', port))
data, adrr = sock.recvfrom(BUFFSIZE)
print("Server says:", data.decode())
