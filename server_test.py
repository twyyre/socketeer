from server import Server
from time import sleep

server = Server()
print("server ip:", server.ip)
server.listen()
sleep(1)
print("send")
server.send("asadasdasdas")


