import socket
import threading

HEADER = 1024
PORT = 5050
HOST_IP = socket.gethostbyname(socket.gethostname())
ADDR = (HOST_IP, PORT)
DECODE_FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
FORMAT = "utf-8"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(ADDR)
print("Connected to chat server")

# sending a message functionality
def send_msg():
    while True:
        message = input(str(""))
        message = message.encode()
        server.send(message)
        print("\nmessage has been sent...")

# receive a message functionality
def recv_msg():
    while True:
        incoming_message = server.recv(HEADER)
        incoming_message = incoming_message.decode(DECODE_FORMAT)
        print("\n>>>"+incoming_message)

# confirm that both users are connected, and run recv_msg and send_msg simultaneously
def communicate():
    incoming_server_message = server.recv(HEADER)
    incoming_server_message = incoming_server_message.decode(FORMAT)
    print(incoming_server_message)
    thread1 = threading.Thread(target=send_msg)
    thread2 = threading.Thread(target=recv_msg)
    thread2.start()
    thread1.start()


communicate()
