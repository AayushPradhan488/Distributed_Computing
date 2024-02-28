import socket

host = '127.0.0.1'
port = 5000

master_server = socket.socket()

def fact(n):
    if n==2:
        return 2
    return n*fact(n-1)

master_server.bind((host, port))
# Start listening to requests
master_server.listen(10)
conn, addr = master_server.accept()
print(f'Connection from: {addr}')
while True:
    print('Receving')
    data = conn.recv(1024).decode()
    if data == 'END':
        print(f'Connection ended')
        break
    x = fact(int(data))
    conn.send(str(x).encode())
    print(f'Data received: {data} sending factorial = {x}')
    break

conn.close()

print('Success!')