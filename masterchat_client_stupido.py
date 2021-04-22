import socket

HOST = ""
PORT = 3313

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind((HOST,PORT))
sock.sendto(b'NICK_REMOTO', ('127.0.0.1', 3333))
while True:
    data, addr = sock.recvfrom(1024)
    print("Ricevuto: " + data.decode())
    message = input()
    sock.sendto(message.encode(), (addr[0], addr[1]))
