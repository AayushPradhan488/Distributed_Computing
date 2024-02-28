import socket

host = '127.0.0.1'
port = 5000

client_server = socket.socket()
client_server.connect((host, port))

#client_server.bind((host, port))
client_server.send('5'.encode())

data = client_server.recv(1024).decode()

print(data)

client_server.close()

print('Success!')