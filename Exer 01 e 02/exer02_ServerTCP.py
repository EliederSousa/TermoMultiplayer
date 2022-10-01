import socket #importa modulo socket
import threading

num_Cliente = [] 
TCP_IP = '192.168.15.174' # endereço IP do servidor 
TCP_PORTA = 42019      # porta disponibilizada pelo servidor
TAMANHO_BUFFER = 1024     # definição do tamanho do buffer
 
# Criação de socket TCP
# SOCK_STREAM, indica que será TCP.
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# IP e porta que o servidor deve aguardar a conexão
servidor.bind((TCP_IP, TCP_PORTA))

#Define o limite de conexões. 
servidor.listen(1)

def BroadCast(data):
    print ("teste")
    global num_Cliente
    for w in num_Cliente:
        w.send(data)

def ThreadingCliente(conn):
    global num_Cliente
    num_Cliente.append(conn)
    while True:
        data = conn.recv(TAMANHO_BUFFER)
        if data: 
            print ("Mensagem recebida:", data)
            BroadCast(data)

print ("Servidor dispoivel na porta 42019 e escutando.....") 

while True:
    conn, addr = servidor.accept()
    threading.Thread(target = ThreadingCliente, args = (conn,) ).start()
    print ('Endereço conectado:', addr)
