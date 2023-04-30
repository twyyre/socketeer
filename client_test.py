from client import Client

client = Client("192.168.1.104")
client.connect()
client.send(client.name)
client.receive()
client.close()