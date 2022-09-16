'''
Date: 20022.06.07
Title:
By: KangJinSEong
'''

import socket

# TCP_client_easy.py
# Create_connection()

port = 2500
address = ("30.0.1.31", port)
BUFSIZE = 1024

s = socket.create_connection(address)


while True:
    msg = input(" Message to send:")
    s.sendall(msg.encode())
    r_msg = s.recv(BUFSIZE)
    if not r_msg:
        break
    print("Received message: %s" %r_msg.decode())
    
s.close()
