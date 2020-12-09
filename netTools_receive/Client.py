import struct
import json
import socket
import subprocess

Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_port = ('127.0.0.1', 8001)
Client.connect(ip_port)

while True:
    msg = input('please input cmd>>> ')
    if len(msg) == 0:
        continue
    if msg == 'quit':
        break
    print('you send: ', msg)
    Client.send(msg.encode('utf-8'))

    length = Client.recv(4)
    length = struct.unpack('i', length)[0]
    print(type(length), ' ', length)
    msg_len = 0
    msg = b''
    while msg_len < length:
        rec = Client.recv(1024)
        msg += rec
        msg_len += len(rec)
    print(msg.decode('gbk'))
