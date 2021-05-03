'''
to do:
    gestire se non trovo client in connect

'''

import socket
import sys, json
from _thread import *

#HOST = str(sys.argv[1])
#PORT = int(sys.argv[2])
HOST = ''
PORT = 3330

CLIENT={'tizio':('127.0.0.1',3311),'caio':('127.0.0.1',3312),'sempronio':('127.0.0.1',3313)}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket creato')

try:
    s.bind((HOST, PORT))
    print('Socket bind completato')
except socket.error as msg:
    print("Bind fallita. Codice di errore: " + str(msg[0]) + " Messaggio " + msg[1])
    sys.exit()

s.listen(10)
print("Socket in ascolto")

def clientthread(conn):

    global CLIENT
    result=""

    data = conn.recv(1024)
    #print('\r\nData: ' + data.decode())
    #print(json.loads(data.decode()))
    data = json.loads(data.decode())
    combo = (data['IP'], data['PORT'])
    #print(combo)
    #print('\r\nCombo: ' + str(combo) + '\r\n')
    for k in CLIENT:
        if k == data['NICK']:
            print("\r\nERR: il client " + data['NICK'] + " è già presente")
            err_message = '\r\nERR: il client ' + data['NICK'] + ' è già presente'
            conn.send(err_message.encode())
            conn.close()
            return
    
    CLIENT[data['NICK']] = combo
    #ciclo for per elenco utenti connessi
    for k in CLIENT:
        result += "\r\n"+ k + ": indirizzo " + CLIENT[k][0] + " porta " + str(CLIENT[k][1])
    print("\r\nElenco client attualmente disponibili:" + result)
    NICK_REM = data['NICK']
    CONN_REM = (data['IP'],data['PORT'])
    #print(NICK_REM, CONN_REM)
    print("\r\nIl client " + NICK_REM + " " + str(CONN_REM) + " è stato registrato")
    conn.send(b'\r\nCiao dati registrati')    
    
    while True:

        data = conn.recv(1024)
        print('\r\nRicevuto il seguente comando: ' + data.decode())
        result=""
        
        #!elenco al primo è gia stringa
        if data[:7].decode() == "!elenco":
            print("\r\nRichiesto elenco client")
            #ciclo for per elenco utenti connessi
            for k in CLIENT:
                result += "\r\n" + k + ": indirizzo " + CLIENT[k][0] + " porta " + str(CLIENT[k][1])
            print(result)
            #print('\r\nSto inviando il primo leenco') 
            conn.send(result.encode())
            #conn.send(b'\r\nElenco client\r\n')

        #!quit
        if data[:5].decode() == "!quit":
            print(NICK_REM + " " + str(CLIENT[NICK_REM]) + " ci ha lasciato con quit.")
            del CLIENT[NICK_REM]
            for k in CLIENT:
                result += "\r\n" + k + ": indirizzo " + CLIENT[k][0] + " porta " + str(CLIENT[k][1])
            print(result)
            conn.send(result.encode() + b'\r\nAddio\r\n')
            conn.close
            break
        
        #!connect nome
        if data[:8].decode() == "!connect":
            nome = data[9:].decode()
            print("\r\n" + NICK_REM + " si vuole connettere con " + nome)
            #print(nome)
            #cerco chiave "nome" in CLIENT
            if nome in CLIENT:
                #restituisco i parametri
                PARAM = {'NICK':nome,'IP':CLIENT[nome][0],'PORT':CLIENT[nome][1]}
                print("\r\nEcco i paramentri di " + nome +  ":\r\n" + str(PARAM) +  ":\r\n" )
                conn.send(json.dumps(PARAM).encode())

            else:
                print(nome + " non è disponibile")
                result = nome + " non disponibile"
                conn.send(result.encode() + b'\r\n')

        #Dracarys
        if data[:9].decode() == "!dracarys":
            print(str(addr[1]) + " ci ha lasciato Dracarys.")
            del CLIENT[str(addr[1])]
            for k in CLIENT:
                result += "\r\n" + k + ": indirizzo " + CLIENT[k][0] + " porta " + str(CLIENT[k][1])
            conn.send(result.encode() + b'\r\nAddio\r\n')
            conn.close
            s.close
            break

    conn.close()

while 1:
    conn, addr = s.accept()
    print('Connesso con ' + addr[0] + ':' + str(addr[1]))
    #print(conn)
    
    start_new_thread(clientthread,(conn,))

s.close()

