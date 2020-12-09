import socket

client = {'danny': '11111111',
          'tony': '22222222',
          'marry': '33333333'}

server = socket.socket()
ip_port = ('127.0.0.1', 8001)
server.bind(ip_port)
server.listen(4)

print('wait for connect...')
conn, addr = server.accept()
print('connect successfully!')

while True:
    info_name_pwd = conn.recv(1024)
    info_name_pwd = info_name_pwd.decode('utf-8')
    name, pwd = info_name_pwd.split()
    #print(name, ' ', pwd)
    if (name in client) and (pwd == client[name]):
        conn.send('good'.encode('utf-8'))
    else:
        conn.send('error'.encode('utf-8'))
        continue

    # log in
    print(name, 'connect successfully!')

    # option
    while True:
        msg = conn.recv(1024)
        msg = msg.decode('utf-8')
        if msg == 'quit':
            break
        option, path = msg.split()
        if option == 'upload':
            open(path, 'w').close()
            conn.send('good'.encode('utf-8'))
        else:
            conn.send('error'.encode('utf-8'))

conn.close()
server.close()
