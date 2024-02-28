import socket
from datetime import datetime

host = '127.0.0.1'
port = 5000

client_server = socket.socket()
client_server.connect((host, port))

#client_server.bind((host, port))
client_server.send(str(datetime.now()).encode())

ts = client_server.recv(1024).decode()

print(f'Timestamp received: {ts}')

client_server.close()

print('Success!')