import socket

HOST = "127.0.0.1"
PORT = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.sendto(b"Invio di prova", (HOST, PORT))
