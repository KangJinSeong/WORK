'''
Date: 20022.06.07
Title:
By: KangJinSEong
'''

import socket

# TCP_client_demo.py
# Simple TCP client

port = 2500
address = ("30.0.1.17", port)
BUFSIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(address)


while True:
    msg = input(" Message to send:")
    s.send(msg.encode())
    r_msg = s.recv(BUFSIZE)
    if not r_msg:
        break
    print("Received message: %s" %r_msg.decode())