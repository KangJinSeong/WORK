'''
Date: 20022.06.08
Title:
By: KangJinSeong
'''

import socket

s_sock = socket.socket()
host = '30.0.1.31'
port = 2500

s_sock.connect((host,port))  # connect server
s_sock.send("I am read".encode())
fn = s_sock.recv(1024).decode() # dadfadf

with open('e:'+fn, 'wb') as f:
    print('file opened')
    print('receiving file...')
    while True:
        data = s_sock.recv(8192)
        if not data:
            break
        f.write(data)
print('Download complete')
s_sock.close()
print('Connection closed')
