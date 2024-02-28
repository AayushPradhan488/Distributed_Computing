import socket
from datetime import datetime

host = '127.0.0.1'
port = 5000

master_server = socket.socket()

master_server.bind((host, port))
# Start listening to requests
master_server.listen(10)
conn, addr = master_server.accept()
print(f'Connection from: {addr}')

ts_client = conn.recv(1024).decode()
print(f'ts_client = {ts_client}\t{type(ts_client)}')
ts_client = datetime.strptime(ts_client, "%Y-%m-%d %H:%M:%S.%f")
ts_master = datetime.now()

time_diff = (ts_master - ts_client)/2

current_clock = ts_master + time_diff

conn.send(str(current_clock).encode())

print(f'Time reset {current_clock}\nSent to client')

'''while True:
    print('Receving')
    data = conn.recv(1024).decode()
    if data == 'END':
        print(f'Connection ended')
        break
    conn.send(str('OK').encode())
    print(f'Timestamp received: {data} sending OK')
    break'''

conn.close()

print('Success!')