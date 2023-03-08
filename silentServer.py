import socket
from datetime import datetime
# connect with client
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.sendto("hello client".encode("utf-8"), ('127.0.0.1', 12345))
