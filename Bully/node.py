import socket
from datetime import datetime
import time

trigger = False

priority_number = 1

# Global variables to store high priority and low priority nodes
high_nodes = []
low_nodes = []

listen_port = 5000

received_data_queue = queue.Queue()

timeout_queue = 60

coordinator = None

class Node:
    def __init__(self, ip_address, priority_number):
        self.ip_address = ip_address
        self.priority_number = priority_number

def send_message(node, message):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((node.ip_address, listen_port))
            s.sendall(message.encode())
    except Exception as e:
        print(f"Error occurred while sending message: {e}")

def send_message_high(message):
    try:
        for node in high_nodes:
            send_message(node, message)
    except Exception as e:
        print(f"Error occurred while sending message to high priority nodes: {e}")

def send_message_all(message):
    try:
        for node in high_nodes + low_nodes:
            send_message(node, message)
    except Exception as e:
        print(f"Error occurred while sending message to all nodes: {e}")

def listen(ip_address, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((ip_address, port))
            s.listen()
            print(f"Node listening on {ip_address}:{port}")
            while True:
                conn, addr = s.accept()
                with conn:
                    print(f"Connected by {addr}")
                    while True:
                        data = conn.recv(1024).decode()
                        if not data:
                            break
                        received_data_queue.put((data, port))
                        print(f"Received data: {data}")
    except Exception as e:
        print(f"Error occurred while listening: {e}")

def election(sender):
    message = "ELECTION"
    if sender!=None:
        send_message(sender, "OK")
    if len(high_nodes) != 0:
        send_message_high(message)
    else:
        send_message_all("COORDINATOR")
        coordinator = True
        return
    t1 = datetime.now()
    return t1

def start_listening(listen_list):
    for i in listen_list:
        i.start()

def main():
    listening_threads = []
    
    # Start listening thread
    node1 = Node(ip_address='192.168.29.111', priority_number=2)
    listen_node1 = Thread(target=listen, args=('192.168.29.111', listen_port))
    listening_threads.append(listen_node1)

    node2 = Node(ip_address='192.168.29.41', priority_number=3)
    listen_node2 = Thread(target=listen, args=('192.168.29.41', listen_port))
    listening_threads.append(listen_node2)

    node3 = Node(ip_address='192.168.29.56', priority_number=4)
    listen_node3 = Thread(target=listen, args=('192.168.29.56', listen_port))
    listening_threads.append(listen_node3)

    #start listening to others
    start_listening(listening_threads)

    if trigger:
        time.sleep(3)
        t1 = election(None)
        data = None
        port = None
        while datetime.now() - t1 < timeout_queue:
            pass
        while not received_data_queue.empty():
            data, port = received_data_queue.get(timeout=5)
            if data == "COORDINATOR":
                for i in [*high_nodes, *low_nodes]:
                    if port == i.ip_address:
                        coordinator = i
                        break
            if data == "OK":
                pass
            if data == None:
                send_message_all("COORDINATOR")
    else:
        while coordinator == None:
            if not received_data_queue.empty():
                data, port = received_data_queue.get(timeout=5)
                if data == "ELECTION":
                    for i in low_nodes:
                        if port == i.ip_address:
                            node = i
                            break
                    t1 = election(node)
                    data_n = None
                    port_n = None
                    while datetime.now() - t1 < timeout_queue:
                        pass
                    while not received_data_queue.empty():
                        data_n, port_n = received_data_queue.get(timeout=5)
                        if data_n == "COORDINATOR":
                            for i in [*high_nodes, *low_nodes]:
                                if port_n == i.ip_address:
                                    coordinator = i
                                    break
                        if data_n == "OK":
                            pass
                        if data_n == None:
                            send_message_all("COORDINATOR")
                if data == "COORDINATOR":
                    for i in [*high_nodes, *low_nodes]:
                        if port == i.ip_address:
                            coordinator = i
                            break

if __name__ == "__main__":
    main()
