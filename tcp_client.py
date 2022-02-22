# Simple TCP Client

import socket

target_host = "0.0.0.0"
target_port = 9998

# creating socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connecting the client
client.connect((target_host,target_port))

# sending data
client.send(b"ABC123")

# receiving data
response = client.recv(4096)

print(response.decode())
client.close()

# full 'socket' documentation @ http://docs.python.org/3/library/socket.html

