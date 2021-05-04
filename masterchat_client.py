import socket, sys, json
from _thread import *

#memorizzo dati del client e inizializzo variabili
NICK = str(sys.argv[1])
CONN = (str(sys.argv[2]), int(sys.argv[3]))
NICK_REM = ""
CONN_REM = ()
IMPEGNATO = False
PARAM = {'NICK':NICK,'IP':str(sys.argv[2]),'PORT':sys.argv[3]}

#creo socket tcp per il server
try:
    st = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket Creato')
except socket.error as msg:
    print('Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1])
    sys.exit();

#creo connessione con il server
st.connect(("127.0.0.1", 3310))
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

print("\r\nELENCO COMANDI DISPONOBILI: \
                \r\n!help --> mostra questo elenco \
                \r\n!elenco --> ritorna elenco client disponibili \
                \r\n!connect <client> --> avvia una chat con l'utente client \
                \r\n!disconnect --> disconnette l'attuale chat \
                \r\n!quit --> esce dal programma")
print('\r\nRICHIESTO ELENCO CLIENT CONNESSI...')

#chiedo elenco client
st.sendall(b'!elenco')
print(st.recv(1024).decode())

#creo socket udp in ascolto e lancio thread
su = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
su.bind(CONN)

#definisco thread udp in ascolto
def server_udp():
    print("\r\nSocket UDP in attesa connessione")
    global IMPEGNATO, NICK_REM, CONN_REM
    while True:
        data, addr = su.recvfrom(1024)
    
    #va in loop - in caso eliminare while
        if IMPEGNATO == True:
            if CONN_REM==addr:
                #sono impeganto con lui quindi verifico opzioni
                if data[:11].decode()=="!disconnect":
                    print("\r\nHai deciso di andartene!")
                    su.sendto(b'disconnect', CONN_REM)
                    IMPEGNATO == False
                    CONN_REM = ()
                    NICK_REM = ""
                    data = su.recv(1024)      
                    print(data.decode())
                    break
                else:    
                    print(NICK_REM + " > " + data.decode())
            else:
                message = '\r\nCiao ' + NICK_REM + ', mi dispiace non sono disponibile'
                su.sendto(message.encode() , addr)
        #verifico se già impegnato in chat e modifico valore
        if IMPEGNATO == False:
            print('\r\nStampo dati prima connessione: ' + data.decode())       
            IMPEGNATO = True
            
            #memorizzo dati client remoto
            if NICK_REM=="":
                NICK_REM = data.decode()
            CONN_REM = addr
            
            #rispondo connessione accettata
            message = '\r\nCiao ' + NICK_REM + ', benvenuto!\r\n'
            print("\r\nSei collegato con: " + NICK_REM + str(CONN_REM))
            su.sendto(message.encode(), CONN_REM)

        
start_new_thread(server_udp ,())

while True:
    cmd = input("\r\nSocket TCP in attesa comando: ")
    print('Ho inserito comando nel thread principale')

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
        st.send(cmd.encode())
        print("\r\nRichiesti dati connessione per " + nome)
        data = st.recv(1024)
        if data[-17:-2].decode()=="non disponibile":
            print(nome + " non è disponibile")
            break
        data = json.loads(data.decode())
        CONN_REM = (data['IP'], data['PORT'])
        NICK_REM = data['NICK']
        print(data)
        su.sendto(NICK.encode(), (data['IP'], int(data['PORT'])))
        IMPEGNATO == True
     
    #!disconnect
    if cmd[:11] == "!disconnect":
        print("\r\nHai deciso di concludere la chat")
        su.sendto(b'disconnect', CONN_REM)
        IMPEGNATO == False
        CONN_REM = ()
        NICK_REM = ""
        data = su.recv(1024)      
        print(data.decode())                
             
    if cmd[:1]!="!":
         su.sendto(cmd.encode(), CONN_REM)