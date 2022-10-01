from concurrent.futures import thread
import socket, pickle
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading
import fsm


"""            //=======\\
               ||       ||
               \/       ||
> login ==> gameloop    ||
    ||         ||       ||
    ||         \/       ||
    \\====> waiting ====// """


fsm = fsm.FiniteStateMachine()
fsm.createState("login", ["gameloop", "wait"])
fsm.createState("gameloop", ["wait"])
fsm.createState("wait", ["gameloop"])
fsm.changeState("login")
state = fsm.getState()


class ClienteInfo:
    nome = ""
    addr = ""
    info = ""
    text = ""


class ServerInfo:
    info = ""
    code = ""
    seg  = ""


client = ClienteInfo()
sock = ""
clientSocket = ""
waitingInfo = ""

# Checa se a entrada é valida. 
def entry_checkLetter( ev, widget, linha ):
    if ev.keysym.isalpha():
        widget.delete(1, 'end')
        text = widget.get()
        if text.isalpha():
            text = text.upper()
            widget.delete(0, 'end')
            widget.insert(0, text)
            if len(cells[linha][0].get()) > 0 and len(cells[linha][1].get()) > 0 and len(cells[linha][2].get()) > 0 and len(cells[linha][3].get()) > 0 and len(cells[linha][4].get()) > 0:
                palavra = cells[linha][0].get() + cells[linha][1].get()  + cells[linha][2].get()  + cells[linha][3].get()  + cells[linha][4].get() 
                enviarPalavra(palavra)
        else:
            widget.delete(0, 'end')

def enviarPalavra( palavra ):
    client.text = palavra
    client.info = "gameloop"
    sock.send(pickle.dumps(client))
    
    #data, addr = sock.recvfrom(2048)
    #data = pickle.loads(data)

def entry_checkName( ev, widget ):
    widget.delete(10, 'end')
    text = widget.get()
    if not text.isalpha() and (len(text) > 0):
        widget.delete(0, 'end')
        messagebox.showerror("Erro", "Use somente letras maíusculas ou minúsculas!")

# Função que cia uma thread e possibilita o recebiment ode mensagens do servidor.
# Com ela, o servidor sempre tem uma confirmação de que o cliente está logado e não dá erro de desconexão.
def clientThread():
    global guesses, waitingForNewRow, fsm, waitingInfo
    print("Thread criada para o cliente {}".format(client.addr))
    while True:
        data = sock.recv(2048)
        data = pickle.loads(data)
        
        if fsm.getState() == "wait":
            if data.info == "gameloop":
                fsm.changeState("gameloop")
            else:
                waitingInfo = data.info
            
        if data.code == 900:
            guesses = data.info
            waitingForNewRow = True
        elif data.code == 910 and not (fsm.getState() == "wait") :
            fsm.changeState("wait")
        #print(data.info)
        #client.info = "ping"
        #sock.send(pickle.dumps(client))
        

def btn_login_callback( nome, ip ):
    global sock, client
    # Cria a conexão com o servidor
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.ioctl(socket.SIO_KEEPALIVE_VALS, (1,10000,3000))
    sock.connect((ip, 30000))

    # Prepara os dados de login e envia
    client.nome = nome
    client.addr = ip
    client.text = ""
    client.info = "login"
    sock.send(pickle.dumps(client))

    # Recebe os dados de confirmação de login
    data, addr = sock.recvfrom(2048)
    data = pickle.loads(data)

    # Checa se o servidor aceitou a conexão
    if data.code == 200:
        messagebox.showinfo("Login", "Conectado")
        fsm.changeState("gameloop")
        (threading.Thread(target=clientThread)).start()
    elif data.code == 404:
        messagebox.showerror("Erro!", "Você já está conectado. ;)")
        sock.close()
    elif data.code == 502:
        messagebox.showerror("Erro!", "Servidor cheio, desculpe :(")
        sock.close()


# Guarda handlers para cada caixa de texto
cells = []
def createrow( placeholder, n ):
    # Cria um frame (container)
    frame = ttk.Frame(placeholder, height=200, padding=10)
    frame.pack()

    temp = []
    # Caixas de texto
    # Não funciona dentro de um loop. Dá conflito nos nomes dos widgets.
    btn1 = tk.Entry(frame, width=2, justify = 'center', font=('consolas', 30, 'bold') )
    btn1.bind("<KeyRelease>", lambda event: entry_checkLetter(event, btn1, n))
    btn1.pack(side='left')
    temp.append(btn1)

    btn2 = tk.Entry(frame, width=2, justify = 'center', font=('consolas', 30, 'bold') )
    btn2.bind("<KeyRelease>", lambda event: entry_checkLetter(event, btn2, n))
    btn2.pack(side='left')
    temp.append(btn2)

    btn3 = tk.Entry(frame, width=2, justify = 'center', font=('consolas', 30, 'bold') )
    btn3.bind("<KeyRelease>", lambda event: entry_checkLetter(event, btn3, n))
    btn3.pack(side='left')
    temp.append(btn3)

    btn4 = tk.Entry(frame, width=2, justify = 'center', font=('consolas', 30, 'bold') )
    btn4.bind("<KeyRelease>", lambda event: entry_checkLetter(event, btn4, n))
    btn4.pack(side='left')
    temp.append(btn4)

    btn5 = tk.Entry(frame, width=2, justify = 'center', font=('consolas', 30, 'bold') )
    btn5.bind("<KeyRelease>", lambda event: entry_checkLetter(event, btn5, n))
    btn5.pack(side='left')
    temp.append(btn5)

    cells.append(temp)

def disableRow( n ):
    for w in range(5):
        cells[n][w].config(state='disabled')

def colorRow( n, guesses ):
    global cells
    for w in range( 5 ):
        if guesses[w] == "c":
            cells[n][w].config(bg='#90ee90')
            cells[n][w].config(disabledbackground="#90ee90")
        elif guesses[w] == "q":
            cells[n][w].config(bg='yellow')
            cells[n][w].config(disabledbackground="yellow")


###############################################################
#### FUNÇÕES DOS ESTADOS DO JOGO ##############################

def login():
    root = tk.Tk()
    root.geometry("300x100")
    root.title('CONECTE AO TERMO')
    root.resizable(0, 0)
    # root.configure(background = 'black') #Caso essa linha dê problema há uma possivel solução abaixo
    #https://stackoverflow.com/questions/10887762/python-tkinter-root-window-background-configuration
    
    # GRID
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=3)

    # Apelido
    username_label = ttk.Label(root, text="Seu apelido (até 10 letras):")
    username_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5) 
    username_entry = ttk.Entry(root)
    username_entry.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)
    username_entry.bind("<KeyRelease>", lambda event: entry_checkName(event, username_entry))
    username_entry.insert(0, "Elieder")

    # IP
    IP_label = ttk.Label(root, text="IP do servidor:")
    IP_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
    IP_entry = ttk.Entry(root)
    IP_entry.insert(0, "192.168.1.105")
    IP_entry.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)

    # Botão
    login_button = ttk.Button(root, text="CONECTAR!", \
        command= lambda: btn_login_callback(username_entry.get(), IP_entry.get()))
    login_button.grid(column=1, row=3, sticky=tk.E, padx=5, pady=5)

    while True:
        # não fazer tk.mainloop() pois ele bloqueia a execução.
        # use um loop infinito, e chame root.update()
        root.update()
        if fsm.getState() == "gameloop":
            break
    
    root.destroy()
    gameloop()

waitingForNewRow = False
tries = 0
guesses = ""

def gameloop():
    global cells, waitingForNewRow, tries, guesses, waitingInfo

    tries = 0
    
    root = tk.Tk()
    root.geometry('400x500')
    root.title(client.nome)
    
    cells = []
    createrow(root, tries)

    while True:
        if waitingForNewRow:
            waitingForNewRow = False
            tries += 1
            if( tries < 6 ):
                colorRow( tries-1, guesses)
                disableRow( tries-1 )
                createrow(root, tries)
            else:
                waitingInfo = "Você perdeu, espere a próxima rodada começar."
                fsm.changeState("wait")

        root.update()
        if fsm.getState() == "wait":
            break
    
    root.destroy()
    wait()
    
    
def wait():
    global waitingInfo
    """
    for m in cells:
        for n in m:
            n.unbind()"""
    
    root = tk.Tk()
    root.geometry("300x300")
    root.title('Aguarde a próxima rodada')
    root.resizable(0, 0)
    # root.configure(background = 'black') #Caso essa linha dê problema há uma possivel solução abaixo
    #https://stackoverflow.com/questions/10887762/python-tkinter-root-window-background-configuration
    
    # GRID

    # Apelido
    info_label = ttk.Label(root)
    info_label.pack()
    
    while True:
        # não fazer tk.mainloop() pois ele bloqueia a execução.
        # use um loop infinito, e chame root.update()
        info_label.config(text=waitingInfo)
        
        root.update()
        if fsm.getState() == "gameloop":
            break
    
    root.destroy()
    gameloop()


login()
