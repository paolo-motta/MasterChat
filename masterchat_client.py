'''
to do:
    gestire se client occupato (c'è già?)

'''

import socket, sys, json
from _thread import *

#memorizzo dati del client e inizializzo variabili
NICK = str(sys.argv[1])
CONN = (str(sys.argv[2]), int(sys.argv[3]))
#NICK = "pippo"
#HOST = "127.0.0.1"
#PORT = 3316
NICK_REM = ""
CONN_REM = ()
IMPEGNATO = False
PARAM = {'NICK':NICK,'IP':str(sys.argv[2]),'PORT':sys.argv[3]}
#PARAM = {'NICK':NICK,'IP':HOST, 'PORT':PORT}
#NICK = "pippo"
#HOST = "127.0.0.1"
#PORT = 3330

#creo socket tcp per il server
try:
    st = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket Creato')
except socket.error as msg:
    print('Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1])
    sys.exit();

#creo connessione con il server
st.connect(("127.0.0.1", 3330))
print("Server Socket Connected")

#invio parametri del client al server
print(PARAM)
st.sendall(json.dumps(PARAM).encode())
data = st.recv(1024).decode()

#if errore chiudo
#!quit
if data[:6] == "\r\nERR:":
    print(data)
    st.close()  
    sys.exit()         

#print('\r\ninviati parametri nick e conn')
#stampo conferma arrivo dati
#print(st.recv(1024).decode())
#chiedo elenco client al server
st.sendall(b'!elenco')
print('\r\nin attesa elenco')
print(st.recv(1024).decode())

#creo socket udp in ascolto e lancio thread
su = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
su.bind(CONN)

#definisco thread udp in ascolto
def server_udp():
    print("\r\nSocket UDP in attesa connessione")
    global IMPEGNATO, NICK_REM, CONN_REM
    data, addr = su.recvfrom(1024)

    #verifico se già impegnato in chat e modifico valore
    if IMPEGNATO == False:
        print('\r\nStampo dati prima connession: ' + data.decode())       
        IMPEGNATO = True
        
        #memorizzo dati client remoto
        NICK_REM = data.decode()
        CONN_REM = addr
        
        #rispondo connessione accettata
        message = '\r\nCiao ' + NICK_REM + ', benvenuto!\r\n'
        print(NICK_REM + str(CONN_REM))
        su.sendto(message.encode(), CONN_REM)
        ''' 
        #entro ciclo di chat ogni ciclo verifico messaggio se comando o no
        while True:
            #attendo connessione da parte di un client
            data, addr = su.recvfrom(1024)
            message = data.decode()
            print("Ricevuto: " + data.decode())
            #verifico se ricevo messaggio di chiusura
            message = input(NICK_REM)
            su.sendto(message.encode(), CONN_REM)

            devo valutare messaggio di chiusura di sua iniziativa o in risposta alla mia
            '''
    else:
        if IMPEGNATO == True:
            if CONN_REM==addr:
                #sono impeganto con lui quindi verifico opzioni
                if data[:11].decode()=="!disconnect":
                    print("\r\nHai deciso di andartene!")
                else:    
                    print(data.decode())
            else:
                message = '\r\nCiao ' + NICK_REM + ', mi dispiace non sono disponibile'
                su.sendto(message.encode() , CONN_REM)
        
start_new_thread(server_udp ,())

#message = input("PRINCIPALE in attesa comando")

while True:
    cmd = input("\r\nSocket TCP in attesa comando: ")
    print('Ho inserito comando nel thread principale')
    #print('\r\n data: ' + data.decode())
    #combo = (addr[0], addr[1])
    #print('\r\n combo: ' + str(combo))
    #CLIENT[str(addr[1])] = combo
    #print(CLIENT)
    #result=""
    #st.send(b'\r\n Ciao dati registrati')

    #!help
    if cmd[:5] == "!help":
        print("\r\nRichiesto elenco comandi")
        print("\r\n!help --> mostra questo elenco \
            \r\n!elenco --> ritorna elenco client disponibili \
            \r\n!connect <client> --> avvia una chat con l'utente client \
            \r\n!disconnect --> disconnette l'attuale chat \
            \r\n!quit --> esce dal programma")

    #!elenco        
    if cmd[:7] == "!elenco":
        st.send(cmd.encode())
        print("\r\nRichiesto elenco")
        data = st.recv(1024)
        print(data.decode())
        #ciclo for per elenco utenti connessi
        #st.send(result.encode() + b'\r\n')
            #conn.send(v)
    #!quit
    if cmd[:5] == "!quit":
        print("\r\nHai deciso di andartene!")
        st.send(cmd.encode())
        data = st.recv(1024)      
        print(data.decode())                
        break
    
    #!connect nome
    if cmd[:8] == "!connect":
        nome = cmd[9:]
        print("\r\nTi vuoi connettere con " + nome)
        #print(nome)
        #cerco chiave "nome" in CLIENT
        st.send(cmd.encode())
        print("\r\nRichiesti dati connessione per " + nome)
        data = st.recv(1024)
        print(data.decode())
        print(data[-17:-2].decode())
        if data[-17:-2].decode()=="non disponibile":
            print(nome + " non è disponibile")
        else:
            data = json.loads(data.decode())
            CONN_REM = (data['IP'], data['PORT'])
            NICK_REM = nome
            print(data)
            su.sendto(NICK.encode(), (data['IP'], int(data['PORT'])))
            IMPEGNATO == True
            while IMPEGNATO == True:
                data = st.recv(1024).decode()
                #if dara errore
                print(data)
                cmd = input("\r\n"+NICK+"> ")
                if cmd[:11] == "!disconnect":
                    print("\r\nHai deciso di andartene!")
                    su.sendto(b'Disconnect', (data['IP'], data['PORT']))
                    IMPEGNATO == False
                    CONN_REM = ()
                    NICK_REM = ""
                    data = st.recv(1024).decode()
                    print(data)
                break
     
    #!disconnect
    if cmd[:11] == "!disconnect":
        print("\r\nHai deciso di concludere la chat")
        su.sendto(b'disconnect', (data['IP'], data['PORT']))
        IMPEGNATO == False
        data = st.recv(1024)      
        print(data.decode())                
             
     