import socket
import sys
from _thread import *

HOST = ""
PORT = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket bind completato')

try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print("Bind fallita. Codice di errore: " + str(msg[0]) + " Messaggio " + msg[1])
    sys.exit()

s.listen(10)
print("Socket in ascolto")


def clientthread(conn):

    conn.send(b"Benvenuto, digita qualcosa: ")

    while True:
        data = conn.recv(1024)
        if data.decode() == "exit\r\n":
            conn.close()
            break
        conn.sendall(b"Ti rispondo con quello che mi hai inviato: " + data)
        conn.send(b"Digita qualcosa - \'exit\' per uscire: ")

    conn.close()


while 1:
    conn, addr = s.accept()
    print('Connesso con ' + addr[0] + ':' + str(addr[1]))

    start_new_thread(clientthread,(conn,))

s.close()
