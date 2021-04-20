import socket, sys

'''
gestire connesisone udp con variabile impegnato
la apro e lanciuo un traed se arriva connessione
altrimenti in attesa comandi

passo argomenti come parametri tupla del thread

'''
NICK = str(sys.argv[1])
HOST = str(sys.argv[2])
PORT = int(sys.argv[3])
#NICK = "pippo"
#HOST = "127.0.0.1"
#PORT = 3330
IMPEGNATO = False

try:
    st = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as msg:
    print('Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1])
    sys.exit();

print('Socket Created')

st.connect(("127.0.0.1", 3330))
print("Server Socket Connected")

#chiedo elenco client
st.send(b'!elenco')
print(st.recv(1024).decode())

while True:
    #inserisco comando
    cmd = input()
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


'''
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
