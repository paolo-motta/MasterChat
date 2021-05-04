import socket
import sys, json
from _thread import *

HOST = ''
PORT = 3310

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
    data = json.loads(data.decode())
    combo = (data['IP'], data['PORT'])
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
            conn.send(result.encode())

        #!quit
        if data[:5].decode() == "!quit":
            print('\r\nAddio a ' + NICK_REM + " " + str(CLIENT[NICK_REM])) 
            del CLIENT[NICK_REM]
            for k in CLIENT:
                result += "\r\n" + k + ": indirizzo " + CLIENT[k][0] + " porta " + str(CLIENT[k][1])
            print('\r\nRimangono disponibili i seguenti client:\r\n' + result)
            conn.send(b'\r\nRimangono disponibili i seguenti client:\r\n' + result.encode() + b'\r\nAddio\r\n')
            conn.close
            break
        
        #!connect nome
        if data[:8].decode() == "!connect":
            nome = data[9:].decode()
            print("\r\n" + NICK_REM + " si vuole connettere con " + nome)

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

    conn.close()

while 1:
    conn, addr = s.accept()
    print('\r\nConnesso con ' + addr[0] + ':' + str(addr[1]))
    #print(conn)
    
    start_new_thread(clientthread,(conn,))

s.close()

