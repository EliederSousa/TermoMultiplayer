from cProfile import run
from msilib.schema import Error
import socket
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import fsm


"""            //=======\\
               ||       ||
               \/       ||
> login ==> gameloop    ||
    ||         ||       ||
    ||         \/       ||
    \\====> waiting ====//

"""
fsm = fsm.FiniteStateMachine()
fsm.createState("login", ["gameloop", "wait"])
fsm.createState("gameloop", ["wait"])
fsm.createState("wait", ["gameloop"])
fsm.changeState("login")

running = True
state = fsm.getState()

def btn_login_callback():
    connected = True
    if connected:
        messagebox.showinfo("Login", "Conectado")
        fsm.changeState("gameloop")
    else:
        messagebox.showerror("showerror", "Error")

def login():

    # root window
    root = tk.Tk()
    root.geometry("300x100")
    root.title('CONECTE AO TERMO')
    root.resizable(0, 0)
    #root.configure(background = 'black')
    
    # configure the grid
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=3)

    # username
    username_label = ttk.Label(root, text="Seu apelido:")
    username_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

    username_entry = ttk.Entry(root)
    username_entry.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)

    # password
    password_label = ttk.Label(root, text="IP do servidor:")
    password_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

    password_entry = ttk.Entry(root)
    password_entry.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)

    # login button
    login_button = ttk.Button(root, text="CONECTAR!", command=btn_login_callback)
    login_button.grid(column=1, row=3, sticky=tk.E, padx=5, pady=5)

    while True:
        # não fazer tk.mainloop() pois ele bloqueia a execução.
        # use um loop infinito, e chame root.update()
        root.update()
        if fsm.getState() == "gameloop":
            break
    
    root.destroy()
    gameloop()    


def createrow( placeholder, n ):
    # This will create a LabelFrame
    frame = ttk.Frame(placeholder, height=200, padding=10)
    frame.pack()
    
    # Caixas de texto
    for w in range(5):
        btn1 = ttk.Entry(frame, width=2, justify = 'center', font=('consolas', 30, 'bold') )
        btn1.pack(side='left')

def gameloop():

    # Creating tkinter window with fixed geometry
    root = tk.Tk()
    root.geometry('400x500')
    # root['bg'] = '#1C1E1F'
    
    createrow(root, 1)
    createrow(root, 2)
    createrow(root, 3)
    createrow(root, 4)
    createrow(root, 5)
    createrow(root, 6)

    while True:
        # não fazer tk.mainloop() pois ele bloqueia a execução.
        # use um loop infinito, e chame root.update()
        root.update()
        if fsm.getState() == "wait":
            break
    
    root.destroy()
    wait()


def wait():
    print("waiting")



#login()
gameloop()

"""
TCP_IP = '192.168.1.104' # endereço IP do servidor 
TCP_PORTA = 30000      # porta disponibilizada pelo servidor
TAMANHO_BUFFER = 2048

MENSAGEM  = "Teste"

# Criação de socket TCP do cliente
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Conecta ao servidor em IP e porta especifica 
cliente.connect((TCP_IP, TCP_PORTA))

# envia mensagem para servidor 
cliente.send(MENSAGEM.encode('UTF-8'))

# recebe dados do servidor 
data, addr = cliente.recvfrom(2048)

# fecha conexão com servidor
cliente.close()

print ("received data:", data)
"""
