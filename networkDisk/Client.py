import socket

client = socket.socket()
ip_port = ('127.0.0.1', 8001)
client.connect(ip_port)

while True:
    name = input('please enter you name and password: ').strip()
    print(name)
    #pwd = input()
    client.send(name.encode('utf-8'))

    ret = client.recv(1024)
    ret = ret.decode('utf-8')
    if ret == 'error':
        continue
    # else
    while True:
        option_path = input(
            'please enter option and path(enter quit to exit): ').strip()
        client.send(option_path.encode('utf-8'))

        if option_path == 'quit':
            break
        msg = client.recv(1024).decode('utf-8')
        if msg == 'good':
            print('execute successfully!')
        else:
            print('fail...')

    # already log in
