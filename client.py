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

def btn_login_callback( nome, ip ):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, 30000))
    sock.send(nome.encode('UTF-8'))
    data, addr = sock.recvfrom(2048)
    sock.close()
    print ("received data:", data, addr)

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
    # root.configure(background = 'black') #Caso essa linha dê problema há uma possivel solução abaixo
    #https://stackoverflow.com/questions/10887762/python-tkinter-root-window-background-configuration
    
    
    
    # configure the grid
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=3)

    # username
    username_label = ttk.Label(root, text="Seu apelido:")
    username_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5) 
    #.grid define a posição de alguma coisa que vc quer inserir(botao, texto e etc)
    #label pedaço de texto incrementado na janela
    username_entry = ttk.Entry(root)
    username_entry.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)

    # password
    IP_label = ttk.Label(root, text="IP do servidor:")
    IP_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

    IP_entry = ttk.Entry(root)
    IP_entry.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)

    # login button
    login_button = ttk.Button(root, text="CONECTAR!", command= lambda: btn_login_callback(username_entry.get(), IP_entry.get()))
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
    #root.configure(bg = 'black')
    root.config(background = 'black')
    
    
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
    # Um layout que terá a seguinte frase: "Fulano acertou. Proxima rodada em x segundos "
    print("waiting")


login()
