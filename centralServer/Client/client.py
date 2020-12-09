import socket
import struct
import json
client = socket.socket()
ip_port = ('127.0.0.1', 8000)
client.connect(ip_port)


def show_menu():
    print('---------------------')
    print('1.log in')
    print('2.sign in')
    print('---------------------')
    print('please choose:')


while True:
    show_menu()
    op = input().strip()
    if op == '1':
        client.send('log in'.encode('utf-8'))
        msg = input('please input account and keys\n')
        client.send(msg.encode('utf-8'))
    elif op == '2':
        client.send('sign in'.encode('utf-8'))
        msg = input('please input account and keys\n')
        client.send(msg.encode('utf-8'))
    else:
        print('enter error!\n')
        continue

    msg = client.recv(1024)
    msg = msg.decode('utf-8')
    if msg == 'good':
        break
    else:
        print(msg+'\n')

print('log in successfully!')

while True:
    option = input('please enter option>>> ')
    client.send(option.encode('utf-8'))
    msg_back = client.recv(1024)
    msg_back = msg_back.decode('utf-8')
    print(msg_back)
    if msg_back == 'copy that!':
        break

header = {'name': 'girl.jpg', 'data_size': 0}

f = open(header['name'], 'rb')
image = f.read()
file_size = len(image)
header['data_size'] = file_size

head_json = json.dumps(header)
head_json_byte = bytes(head_json, encoding='utf-8')
head_len = len(head_json_byte)
#head_len = len(head_json)

client.send(struct.pack('i', head_len))
client.send(head_json_byte)  # bytes?
# client.send(head_json.encode('utf-8'))
client.send(image)
print('excute successfully!')

f.close()
client.close()
