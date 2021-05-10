'''
si potrebbe modificare per inviare sempre un json
poi chi riceve parsa le chiavi e a seconda delle chivi trovate fa cose (magari chiamando funzioni)
gestione chiave DH assegnata o meno
andrà gestita la cancellazione della chiave al disconnect
'''

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from _thread import *
import socket, sys, json, binascii, os

#memorizzo dati del client e inizializzo variabili
NICK = str(sys.argv[1])
CONN = (str(sys.argv[2]), int(sys.argv[3]))
NICK_REM = ""
CONN_REM = ()
IMPEGNATO = False
PARAM = {'NICK':NICK,'IP':str(sys.argv[2]),'PORT':int(sys.argv[3])}
block = algorithms.AES.block_size/8
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
print(st.recv(1024).decode() + '\r\n')

#creo socket udp in ascolto e lancio thread
su = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
su.bind(CONN)

#definisco thread udp in ascolto
def server_udp():
    
    global IMPEGNATO, NICK_REM, CONN_REM
    
    while True:
        data, addr = su.recvfrom(1024)
    
        if IMPEGNATO == True:
            if CONN_REM == addr:
                #sono impeganto con lui quindi verifico opzioni
                if data[:11].decode()=="!disconnect":
                    print("\r\nHa deciso di andarsene!\r\n")
                    su.sendto(b'!disconnect', CONN_REM)
                    IMPEGNATO = False
                    CONN_REM = ()
                    NICK_REM = ""
                    break
                else:    
                    print(NICK_REM + " > " + data.decode() + "\r\n" + NICK + " > ")
            else:
                message = '\r\nCiao ' + NICK_REM + ', mi dispiace non sono disponibile'
                su.sendto(message.encode() , addr)
        
        #verifico se già impegnato in chat e modifico valore
        if IMPEGNATO == False:
            if data[:11].decode()!="!disconnect":
                print('\r\nStampo dati prima connessione: ' + data.decode())       
                IMPEGNATO = True
                
                #memorizzo dati client remoto
                if NICK_REM == "":
                    NICK_REM = data.decode()
                CONN_REM = addr
                
                '''
                ppk = ec.generate_private_key(ec.SECP384R1()).public_key()
                pk = ec.generate_private_key(ec.SECP384R1())
                sk = pk.exchange(ec.ECDH(), ppk)
                dk = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'handshake data',).derive(sk)
                
                iv = os.urandom(block)                
                ctx = padding.PKCS7(8*block).padder()
                padded_pt = ctx.update(pt) + ctx.finalize()
                cipher = Cipher(algorithms.AES(dk), modes.CBC(iv), default_backend())
                ctx = cipher.encryptor()
                ciphertext = ctx.update(padded_plaintext) + ctx.finalize()
                '''

                #rispondo connessione accettata
                message = '\r\nCiao ' + NICK_REM + ', benvenuto!\r\n'
                print("\r\nSei collegato con: " + NICK_REM + str(CONN_REM))
                su.sendto(message.encode(), CONN_REM)
        
start_new_thread(server_udp ,())

while True:
    
    cmd = input(NICK + " > ")

    #nessun input
    if not cmd:
        print("\r\nDevi digitare qualcosa\r\n")
    
    #messaggio in input
    elif cmd[:1]!="!":
        if IMPEGNATO:
            su.sendto(cmd.encode(), CONN_REM)

        else:
            print("\r\nDevi digitare un comando!\r\n")
        
    #!help
    elif cmd[:5] == "!help":
        print("\r\nRichiesto elenco comandi")
        print("\r\n!help --> mostra questo elenco \
            \r\n!elenco --> ritorna elenco client disponibili \
            \r\n!connect <client> --> avvia una chat con l'utente client \
            \r\n!disconnect --> disconnette l'attuale chat \
            \r\n!quit --> esce dal programma\r\n")

    #!elenco        
    elif cmd[:7] == "!elenco":
        st.send(cmd.encode())
        print("\r\nRichiesto elenco")
        data = st.recv(1024)
        print(data.decode() + '\r\n')

    #!quit
    elif cmd[:5] == "!quit":
        print("\r\nHai deciso di andartene!")
        st.send(cmd.encode())
        data = st.recv(1024)      
        print(data.decode())  
        break
    
    #!connect nome
    elif cmd[:8] == "!connect":
        nome = cmd[9:]
        print("\r\nTi vuoi connettere con " + nome)
        st.send(cmd.encode())
        print("\r\nRichiesti dati connessione per " + nome)
        data = st.recv(1024)
        if data[-17:-2].decode()=="non disponibile":
            print(nome + " non è disponibile")
        else: 

        '''
        ppk = ec.generate_private_key(ec.SECP384R1()).public_key()
        pk = ec.generate_private_key(ec.SECP384R1())
        sk = pk.exchange(ec.ECDH(), ppk)
        dk = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b'handshake data',).derive(sk)

        iv = os.urandom(block)                
        ctx = padding.PKCS7(8*block).padder()
        padded_pt = ctx.update(pt) + ctx.finalize()
        cipher = Cipher(algorithms.AES(dk), modes.CBC(iv), default_backend())
        ctx = cipher.encryptor()
        ciphertext = ctx.update(padded_plaintext) + ctx.finalize()
        '''
            
            data = json.loads(data.decode())
            CONN_REM = (data['IP'], data['PORT'])
            NICK_REM = data['NICK']
            print(data)
            su.sendto(NICK.encode(), CONN_REM)
            IMPEGNATO = True
     
    #!disconnect
    elif cmd[:11] == "!disconnect":
        print("\r\nHai deciso di concludere la chat\r\n")
        su.sendto(b'!disconnect', CONN_REM)
        IMPEGNATO = False
        CONN_REM = ()
        NICK_REM = ""
    
    #comando sconosciuto     
    elif cmd[:1]=="!":
        print("\r\nComando non conosciuto.\r\n")
