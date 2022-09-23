import socket
import sys
from _thread import *

MAX_CLIENTS     = 2
DEFAULT_PORT    = 30000

print("\n \
  ________________  __  _______  _____ __________ _    ____________  \n \
 /_  __/ ____/ __ \/  |/  / __ \/ ___// ____/ __ \ |  / / ____/ __ \ \n \
  / / / __/ / /_/ / /|_/ / / / /\__ \/ __/ / /_/ / | / / __/ / /_/ / \n \
 / / / /___/ _, _/ /  / / /_/ /___/ / /___/ _, _/| |/ / /___/ _, _/  \n \
/_/ /_____/_/ |_/_/  /_/\____//____/_____/_/ |_| |___/_____/_/ |_|   \n \
")
print("             Proudly created by Elieder & Jose Team\n")

def getMyIP():
    ip = socket.gethostbyname(socket.gethostname())
    print("IP local:", ip)
    return ip


def socketCreate( ip, porta ):
    print("Criando o servidor...")
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        #if sys.argv[1]:
        # serv.bind((getMyIP(), int(sys.argv[1])))
        #else:
        serv.bind((ip, porta))
        print("Servidor aberto no IP {}.".format(ip, porta))
    except socket.error as e:
        print("Erro:", e)
    return serv


def clientThread( con ):
    while True:
        try:
            data = con.recv(2048)
            reply = data.decode("utf-8")

            if not data:
                print("Cliente no IP {} desconectado".format(con))
                break
            else:
                print("Mensagem:", reply)
            con.sendall(str.encode(reply))
        except:
            print("Deu um pau no sistema")
            break


serv = socketCreate(getMyIP(), DEFAULT_PORT)
serv.listen(MAX_CLIENTS)
print("Servidor ouvindo a porta {}.".format(DEFAULT_PORT))

running = True

while running:
    sock, add = serv.accept()
    start_new_thread(clientThread, (sock,))