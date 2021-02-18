import socket
import threading

HEADER = 1024
PORT = 5050
HOST_IP = socket.gethostbyname(socket.gethostname())
ADDR = (HOST_IP, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# redirect client_1's messages
def client_1_comm(c_1_conn, c_2_conn):
    while True:
        message_c2 = c_2_conn.recv(HEADER)
        c_1_conn.send(message_c2)

# redirect client_2's messages
def client_2_comm(c_1_conn, c_2_conn):
    while True:
        message_c1 = c_1_conn.recv(HEADER)
        c_2_conn.send(message_c1)

# enable messaging between clients
def handle_clients(c_1_conn, c_2_conn):
    thread_c1 = threading.Thread(target=client_1_comm, args=(c_1_conn, c_2_conn))
    thread_c2 = threading.Thread(target=client_2_comm, args=(c_1_conn, c_2_conn))

    thread_c1.start()
    thread_c2.start()

# destructure clients list and run the handle_clients function
def connect_clients(clients):
    print("[SERVER] initializing client connection")
    # destructuring client object
    client_1_conn, client_1_add = clients["1"]
    client_2_conn, client_2_add = clients["2"]
    
    server_msg = "[SERVER] You are connected, feel free to chat now."
    server_msg = server_msg.encode(FORMAT)
    client_1_conn.send(server_msg)
    client_2_conn.send(server_msg)

    thread_handle_clients = threading.Thread(
        target=handle_clients, args=(client_1_conn, client_2_conn))
    thread_handle_clients.start()

# start the server, allow connection, call connect_clients
def start():
    server.listen()
    print(f"[SERVER] LISTENING ON {HOST_IP}...")
    client_pair = {}
    client_id = 1

    while True:
        if (len(client_pair) <= 2):
            conn, address = server.accept()
            client_pair[f"{client_id}"] = conn, address
            client_id += 1
        if len(client_pair) == 2:
            connect_clients(client_pair)


print("[SERVER] server is starting...")
start()
