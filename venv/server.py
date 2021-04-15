import socket
import threading

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECTED"

# ip of this system
# SERVER="192.168.0.144"

# fetches the ip of the system
SERVER = socket.gethostbyname(socket.gethostname())
# print(SERVER)  # prints the ip
# print(socket.gethostname()) #prints the hostname of the ip

ADDR = (SERVER, PORT)  # tuple for binding which should have server ip and port num

# To create new socket, AF_INET: Type of socket like IPv4, SOCK_STREAM: streaming data through socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)  # binding the socket


# handle single connection btw client and server
def handleClient(connection, address):
    print(f"[NEW CONNECTION] {address} connected.")
    connected = True
    while connected:
        msg_length = connection.recv(HEADER).decode(FORMAT)  # waiting to get msg from client before proceeding
        if msg_length:
            msg_length = int(msg_length)
            msg = connection.recv(msg_length).decode(FORMAT)

            if msg == DISCONNECT_MESSAGE:
                connected = False
            print(f"[{address}] {msg}")

    connection.close()


# start function will have logic for our server to start listening and handle those connection and passing to clients
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        connection, address = server.accept()  # wait for new connection to server and store its address and actual object in connection to connect back
        thread = threading.Thread(target=handleClient, args=(connection, address))  # single thread of comm
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...... ")
start()
