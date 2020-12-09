import socketserver
import struct
import json
import os

# current path
const_path = '/Users/xiesicheng/Desktop/project/my_common_project/python/net/centralServer/Repertory/'
cur_path = ''
# dic for storing info
info = {}


def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)


class MyServer(socketserver.BaseRequestHandler):
    def handle(self):
        # log in
        print('connect successfully!')
        self.log_in()
        print('log in successfully!')
        option = self.get_option()
        if option == 'upload':
            self.upload()

    def log_in(self):

        while True:
            op = self.request.recv(1024)
            op = op.decode('utf-8').strip()
            print('option= ', op)
            if op == 'log in':
                # log in
                msg = self.request.recv(1024)
                account, key = msg.decode('utf-8').split()
                print(account, ' ', key)
                if info[account] == key:
                    global cur_path
                    self.request.send(bytes('good', encoding='utf-8'))
                    cur_path = const_path+account+'/'
                    break
                else:
                    self.request.send(bytes('bad match', encoding='utf-8'))
            elif op == 'sign in':
                # sign in
                print('*')
                msg = self.request.recv(1024)
                print('msg= ', msg)
                account, key = msg.decode('utf-8').split()
                print(account, ' ', key)
                if account in info:
                    self.request.send(bytes('account exist', encoding='utf-8'))
                    continue
                info[account] = key
                cur_path = const_path+account+'/'
                mkdir(cur_path)
                self.request.send(bytes('good', encoding='utf-8'))
                break
            else:
                self.request.send(bytes('option error', encoding='utf-8'))
                continue

    def get_option(self):
        # get option
        option = ''
        while True:
            option = self.receive_op().strip()
            if option == 'upload':
                self.request.send(bytes('copy that!', encoding='utf-8'))
                break
            else:
                self.request.send(bytes('error!', encoding='utf-8'))
                continue
        print('get option: ', option)
        # unpack the message
        print('now excute the option')
        return option

    def upload(self):
        name, message = self.receive_mes()
        print('receive successfully!')

        first_name = name[:name.find('.')]
        last_name = name[name.find('.'):]
        name = cur_path+name
        while os.path.exists(name):
            first_name += '1'
            name = cur_path+first_name+last_name
        print(name)
        f = open(name, 'wb')
        f.write(message)
        f.close()
        print('end')

    # private
    def receive_op(self):
        option = self.request.recv(1024)
        option = option.decode('utf-8')
        return option

    def receive_mes(self):
        head_json_len = self.request.recv(4)
        head_json_len = struct.unpack('i', head_json_len)[0]
        head_json_byte = self.request.recv(head_json_len).decode('utf-8')
        head_json = json.loads(head_json_byte)
        data_size = head_json['data_size']
        data_name = head_json['name']

        message = b''
        mes_len = 0
        while mes_len < data_size:
            mes_pack = self.request.recv(1024)
            message += mes_pack
            mes_len += len(mes_pack)
        return data_name, message


if __name__ == "__main__":
    HOST, PORT = "127.0.0.1", 8000

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyServer) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
