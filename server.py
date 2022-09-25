import socket, pickle
from _thread import *
from xmlrpc.client import Server

MAX_CLIENTS     = 2
DEFAULT_PORT    = 30000
DEBUGMODE       = True

clientes = {}
numClientes = 0


class ClienteInfo:
    nome = ""
    addr = ""
    info = ""
    text = ""


class ServerInfo:
    info = ""
    code = ""
    seg  = ""


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
    serv.ioctl(socket.SIO_KEEPALIVE_VALS, (1,60000,1000))
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
    global numClientes
    svInfo = ServerInfo()
    while True:
        try:
            data = con.recv(2048)
            data = pickle.loads(data)

            if not data:
                print("Cliente no IP {} não enviou dados".format(con))
                break
            else:
                if data.info == "login":
                    temp = ServerInfo()
                    temp.code = 200
                    temp.info = "Conectado!"
                    con.send(pickle.dumps(temp))
                elif data.info == "gameloop":
                    print(data.text)

        except:
            print("Deu um pau no sistema")
            break

    numClientes -= 1
    print(con)
    print("Clientes online:", numClientes)


serv = socketCreate(getMyIP(), DEFAULT_PORT)
serv.listen(MAX_CLIENTS)
print("Servidor ouvindo a porta {}.".format(DEFAULT_PORT))

running = True

while running:
    sock, addr = serv.accept()

    if addr[0] in clientes and not DEBUGMODE:
        print("IP {} chutado por tentar se conectar novamente.".format(addr[0]))
        temp = ServerInfo()
        temp.code = 404
        sock.send(pickle.dumps(temp))
    elif numClientes == MAX_CLIENTS:
        temp = ServerInfo()
        temp.code = 502
        sock.send(pickle.dumps(temp))
    else:
        print("\n======== NOVO CLIENTE ========")
        print("IP:", addr[0], ":", addr[1] )
        clientes[addr[0]] = {}
        numClientes += 1
        print("Clientes online:", numClientes)
        start_new_thread(clientThread, (sock,))
