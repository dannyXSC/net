from socket import *
from time import strftime
import time
ip_port = ('127.0.0.1', 9000)
bufsize = 1024

tcp_server = socket(AF_INET, SOCK_DGRAM)
tcp_server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
tcp_server.bind(ip_port)

while True:
    msg, addr = tcp_server.recvfrom(bufsize)
    print('===>', msg)
    stru_time = time.localtime()  # 当前的结构化时间
    if not msg:
        time_fmt = '%Y-%m-%d %X'
    else:
        time_fmt = msg.decode('utf-8')
    back_msg = strftime(time_fmt, stru_time)
    print(back_msg, type(back_msg))
    tcp_server.sendto(back_msg.encode('utf-8'), addr)

tcp_server.close()
