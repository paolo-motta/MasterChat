import socket
import sys, json
from _thread import *

#HOST = str(sys.argv[1])
#PORT = int(sys.argv[2])
HOST = ''
PORT = 3340

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
    '''
    VERIFICARE I DATI DI CONNESSIONE RICEVUTI
    E MEMORIZZARLI
    '''
    data = conn.recv(1024)
    print('\r\nData: ' + data.decode())
    #print(json.loads(data.decode()))
    data = json.loads(data.decode())
    combo = (data['IP'], data['PORT'])
    #print(combo)
    #print('\r\nCombo: ' + str(combo) + '\r\n')
    
    CLIENT[data['NICK']] = combo
    print(CLIENT)
    NICK_REM = data['NICK']
    CONN_REM = (data['IP'],data['PORT'])
    print(NICK_REM, CONN_REM)
    conn.send(b'\r\nCiao dati registrati')    
    
    while True:

        data = conn.recv(1024)
        print('\r\nRicevuto il seguente comando: ' + data.decode())
        result=""
        
        #!elenco al primo è gia stringa
        if data[:7].decode() == "!elenco":
            print("Richiesto elenco")
            #ciclo for per elenco utenti connessi
            for k in CLIENT:
                result += "\r\n" + k + ": indirizzo " + CLIENT[k][0] + " porta " + str(CLIENT[k][1])
            print(result)
            #print('\r\nSto inviando il primo leenco') 
            conn.send(result.encode())
            conn.send(b'\r\nElenco client\r\n')

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

        conn.sendall(b"Ti rispondo con quello che mi hai inviato: " + data)
        conn.send(b"Digita qualcosa - \'exit\' per uscire: ")

        '''

    conn.close()

while 1:
    conn, addr = s.accept()
    print('Connesso con ' + addr[0] + ':' + str(addr[1]))
    print(conn)
    
    start_new_thread(clientthread,(conn,))

s.close()


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
