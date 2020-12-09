import struct
import json
import socket
import subprocess

Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ip_port = ('127.0.0.1', 8001)
Server.bind(ip_port)
Server.listen(3)

while True:
    conn, addr = Server.accept()
    while True:
        cmd = conn.recv(1024)
        print('cmd: ', cmd.decode('utf-8'))
        if not cmd:
            break

        res = subprocess.Popen(cmd.decode('utf-8'),
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        err = res.stderr.read()
        if err:
            msg = err
        else:
            msg = res.stdout.read()
        msg_len = len(msg)
        conn.send(struct.pack('i', msg_len))
        conn.send(msg)
    Server.close()
