import socket

HOST = ""
PORT = 3312

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind((HOST,PORT))

while True:
    data, addr = sock.recvfrom(1024)
    print("Ricevuto: " + data.decode())
    message = input()
    sock.sendto(message.encode(), (addr[0], addr[1]))
