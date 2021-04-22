import socket, sys
from _thread import *

#memorizzo dati del client e inizializzo variabili
NICK = str(sys.argv[1])
CONN = (str(sys.argv[2]), int(sys.argv[3]))
NICK_REM = ""
CONN_REM = ()
IMPEGNATO = False
#NICK = "pippo"
#HOST = "127.0.0.1"
#PORT = 3330

#creo socket tcp per il server
try:
    st = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as msg:
    print('Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1])
    sys.exit();

print('Socket Created')

#creo connessione con il server
st.connect(("127.0.0.1", 3330))
print("Server Socket Connected")

#invio parametri del client al server
param = '('+NICK+'|'+str(CONN)+')'
st.sendall(param.encode())
print('\r\ninviati parametri nick e conn')
#stampo conferma arrivo dati
print(st.recv(1024).decode())
#chiedo elenco client al server
st.sendall(b'!elenco')
print('\r\nin attesa elenco')
print(st.recv(1024).decode())

#creo socket udp in ascolto e lancio thread
su = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
su.bind(CONN)

#definisco thread udp in ascolto
def server_udp():
    print("\r\nSECONDARIO in attesa comando")
    global IMPEGNATO, NICK_REM, CONN_REM
    data, addr = su.recvfrom(1024)
    #print('\r\n\Stampo dati prima connession: 'data.decode())
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
    cmd = input("\r\nPRINCIPALE in attesa comando: ")

    #print('\r\n data: ' + data.decode())
    #combo = (addr[0], addr[1])
    #print('\r\n combo: ' + str(combo))
    #CLIENT[str(addr[1])] = combo
    #print(CLIENT)
    result=""
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
        break
    
    #!connect nome
    if data[:8].decode() == "!connect":
        nome = data[9:].decode()
        print("Si vuole connettere con " + nome)
        #print(nome)
        #cerco chiave "nome" in CLIENT
        if nome in CLIENT:
            #restituisco i parametri
            result = str(CLIENT[nome][0]) + "|" + str(CLIENT[nome][1])
            conn.send(result.encode() + b'\r\n')

        if not nome in CLIENT:
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

      
'''
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print('Connected with ' + addr[0] + ':' + str(addr[1]))
    
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.






while True:
    #inserisco comando
    cmd = input("\r\nPRINCIPALE in attesa comando")
    st.send(cmd.encode())
    #ricevo e stampo risposta
    data = st.recv(1024)
    print(data.decode())
    pos = data.decode().index('|')
    #uscita = data[-7:-2].decode()
    #print(uscita)
    if cmd[:8] == "!connect":
        su = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while True:
            message = input("inserisci messaggio")
            su.sendto(message.encode(), (data[:pos], int(data[pos+1:])))
            messaggio, addr = su.recvfrom(1024)
            print("Ricevuto: " + messaggio.decode())
    
        while True:
            data, addr = sock.recvfrom(1024)
            print("received message:", data)

    sock.sendto(data, (addr[0], addr[1]))
    #!elenco
    if data[-7:-2].decode() == "Addio":
        print("ho decidso di andare via")
        #print(data.decode())
        st.close
        break


#connessione udp
#su = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#su.sendto(b"Invio di prova", (HOST, PORT))


Input da riga di comando
• L’input da riga di comando può essere catturato tramite la lista
sys.argv:
IP = str(sys.argv[1])
PORT = int(sys.argv[2])
NICKNAME = str(sys.argv[3])Caratteri e stringhe
• Per togliere eventuali caratteri di fine stringa al funzione rstrip() può
essere usata
• Per recuperare la posizione di un determinato carattere all’interno di
una stringa, ad esempio per esaminare il messaggio ricevuto, si può
usare la funzione index():
pos = data.index('|')
• Data una posizione all’interno di una stringa, una sottostringa può
essere isolata nel seguente modo:
• pos = data.index('|') # ho una stringa “ciao|pippo”
• sottostringa = data[:pos] # isolo “ciao”
• sottostringa = data[pos+1:] # isolo “pippo”Gestire la stampa in maniera ordinata
• Per gestire la stampa in maniera incrementale si puo’ usare la
sys.stdout.write() che puo’ essere usata per stampare sottostringhe o
caratteri singoli e gestire anche il momento in cui tutti i caratteri
vengono mostrati:
• sys.stdout.write('\n'+NICKNAME+'>')
• sys.stdout.flush() # Stampa tutto a videoVariabili condivise tra thread
• Per avere delle variabili condivise tra uno o più thread delle variabili
globali possono essere utilizzate
• Queste variabili possono essere accedute anche all’interno di un
thread (o in generale una funzione) usando la parola chiave global,
esempio:
def recv_msg():
global remote_host
global remote_portParsare i comandi o i messaggi ricevuti
• Il parsing dei comandi o dei messaggi ricevuti può essere fatto nella
seguente maniera:
if user_input[:9] == "!connect ":
name = user_input[9:].rstrip()
server_s.sendall("who "+str(name))

'''
