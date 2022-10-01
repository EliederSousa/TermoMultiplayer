import socket #importa modulo socket
import threading


TCP_IP = '192.168.15.174' # endereço IP do servidor 
TCP_PORTA = 42019      # porta disponibilizada pelo servidor
TAMANHO_BUFFER = 1024        

# Criação de socket TCP do cliente
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Conecta ao servidor em IP e porta especifica 
cliente.connect((TCP_IP, TCP_PORTA))


def ThreadingEnvio():
    global cliente
    while True:
        MENSAGEM  = input("Digite sua mensagem para o servidor: ")
        cliente.send(MENSAGEM.encode('UTF-8'))

threading.Thread(target = ThreadingEnvio).start()

while True:
    data, addr = cliente.recvfrom(1024)
    print(data.decode('UTF-8'))

# fecha conexão com servidor
cliente.close()

