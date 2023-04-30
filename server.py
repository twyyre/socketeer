import socket
import struct

class Server:
    def __init__(self, _ip=None, _port=12345):
        # Define the IP address and port number to listen on
        if(_ip):
            self.ip = _ip  # replace with the server's IP address
        else:
            self.ip = self.get_ip()

        self.port = _port  # choose a port number

        # Create a TCP/IP socket and bind it to the IP address and port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.ip, self.port))

        self.clients = []
    
    def listen(self, _max_connections=1):
        max_connections = _max_connections
        # Listen for incoming connections and handle each one in a separate thread
        self.server_socket.listen(1)
        print(f"Waiting for incoming connections on {self.ip}:{self.port}...")
        while max_connections > 0:
            client_socket, client_address = self.server_socket.accept()
            self.clients.append(client_socket)
            print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
            # Handle the client connection in a separate thread or process
            # For example, you can use the client_socket object to send/receive data to/from the client
            # Receive data from the server
            received_data = client_socket.recv(1024).decode()
            print(f"Received data from server: {received_data}")
            if(len(self.clients)>=max_connections):
                break
        print("sdasd")

    def send(self, _data):
        message = _data
        for client in self.clients:
            print("client name:", client)
            client.send(message.encode())

    def get_ip(self):

        # get the hostname of the computer
        self.hostname = socket.gethostname()

        # get the IP address associated with the hostname
        self.ip = socket.gethostbyname(self.hostname)

        return self.ip
    
    def broadcast(self):
        BROADCAST_MESSAGE = 'SERVER_DISCOVERY_REQUEST'

        # Create a UDP socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Enable broadcasting mode
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        # Bind the socket to a specific port
        client_socket.bind(('0.0.0.0', self.ip_packed()))

        # Send the broadcast message
        client_socket.sendto(str.encode(BROADCAST_MESSAGE), ('<broadcast>', self.ip_packed()))

        # Receive the server's IP address
        data, server_address = client_socket.recvfrom(1024)

        # Print the server's IP address
        print('Server found at IP address:', data.decode('utf-8'))

    def ip_packed(self):
        #this function is to convert the ip to an int usable with:
        #client_socket.sendto(str.encode(BROADCAST_MESSAGE), ('<broadcast>', self.ip_packed()))
        ip = socket.inet_aton(self.ip)
        ip = struct.unpack('!L', ip)[0]
        return ip
