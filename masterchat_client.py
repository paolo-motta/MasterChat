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
print(st.recv(1024).decode())
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
    print('\r\n\Stampo dati prima connession: ' + data.decode())
    #verifico se già impegnato in cheht e modifico valore
    if IMPEGNATO == False:
       
        IMPEGNATO = True
        
        #memorizzo dati client remoto
        NICK_REM = data.decode()
        CONN_REM = addr
        
        #rispondo connessione accettata
        message = 'Ciao ' + NICK_REM + ', benvenuto!'
        print(NICK_REM + str(CONN_REM))
        su.sendto(message.encode(), CONN_REM)
 
        #entro ciclo di chat ogni ciclo verifico messaggio se comando o no
        while True:
            #attendo connessione da parte di un client
            data, addr = su.recvfrom(1024)
            message = data.decode()
            print("Ricevuto: " + data.decode())
            #verifico se ricevo messaggio di chiusura
            message = input(NICK_REM)
            su.sendto(message.encode(), CONN_REM)
            '''
            devo valutare messaggio di chiusura di sua iniziativa o in risposta alla mia
            '''
            
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

    #!elenco
    if cmd[:7] == "!elenco":
        st.send(cmd.encode())
        print("Richiesto elenco")
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
        data = json.loads(data.decode())
        #combo = (data['IP'], data['PORT'])
        print(data)
        
    #Dracarys
    if cmd[:9] == "!dracarys":
        print(str(addr[1]) + " ci ha lasciato Dracarys.")
        del CLIENT[str(addr[1])]
        for k in CLIENT:
            result += "\r\n" + k + ": indirizzo " + CLIENT[k][0] + " porta " + str(CLIENT[k][1])
        conn.send(result.encode() + b'\r\nAddio\r\n')
        conn.close
        s.close
        break

      