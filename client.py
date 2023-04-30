import socket
from time import sleep

class Client:
    def __init__(self, _server_ip="192.168.1.102", _server_port=12345):
        # Define the IP address and port number to connect to
        self.server_ip = _server_ip  # replace with the server's IP address
        self.server_port = _server_port  # replace with the server's port number

        # Connect to the server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.name = self.get_device_info()["name"]

        self.connection = None

    def connect(self, _tries=1, _delay=1):
        
        tries = _tries
        delay = _delay

        while tries>0:
            try:
                print(f"Connecting to {self.server_ip}:{self.server_port}...")
                self.client_socket.connect((self.server_ip, self.server_port))
                print(f"Connected to {self.server_ip}:{self.server_port}")
                break
            except:
                tries -= 1
                if(tries<=0):
                    raise Exception("Connection failed")
                sleep(delay)
        
    def send(self, _data="Hello, server!"):
        # Send data to the server
        data = _data
        self.client_socket.send(data.encode())

    def receive(self):
        # Receive data from the server
        received_data = self.client_socket.recv(1024).decode()
        print(f"Received data from server: {received_data}")
        return received_data
    
    def listen(self):
        # Create a UDP socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        # Enable broadcasting mode
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        # Bind the socket to a specific port
        self.server_socket.bind(('0.0.0.0', self.server_port))

        print('Server started and listening for broadcast messages...')

        while True:
            data, address = self.server_socket.recvfrom(1024)
            message = data.decode('utf-8')
            
            # Respond with the server's IP address
            if message == 'SERVER_DISCOVERY_REQUEST':
                self.server_socket.sendto(str.encode(socket.gethostbyname(socket.gethostname())), address)

    def get_device_info(self):

        import platform as p
        import os
        import psutil as ps
        
        name = p.node()
        machine = p.machine()
        arch = p.architecture()
        ram = ps.virtual_memory()
        cpu = p.processor()
        system = p.system()
        python = p.python_build()
        platform = p.platform()
        cpu_count = os.cpu_count()
        working_directory = os.getcwd()
        user = os.getlogin()

        client_info = dict()
        client_info["name"]=name
        client_info["machine"]=machine
        client_info["arch"]=arch
        client_info["ram"]=ram
        client_info["cpu"]=cpu
        client_info["system"]=system
        client_info["python"]=python
        client_info["platform"]=platform
        client_info["cpu_count"]=cpu_count
        client_info["working_directory"]=working_directory
        client_info["user"]=user

        return client_info

    def close(self):
        # Close the connection
        self.client_socket.close()
