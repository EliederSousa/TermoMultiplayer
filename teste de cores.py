print('\033[4;31;43m----APRENDENDO A PINTAR NO PYTHON PARA IMPLEMENTAR NO TERMOSERVER----\033[m')
print('\033[0;37;44m----TERMOSERVER----\033[m')
nome = input('\033[1;37;44mDigite seu nome: \033[m')
print('\033[2;32;107m{} \033[m'.format(nome))


#código para cor em python '\033[Estilo da letra; cor da letra; cor do background \033[m'
"""text                    background
 
30      black         preto       40
31      red           vermelho    41
32      green       verde         42
33      yellow      amarelo       43
34      blue          azul        44
35      Magenta  Magenta          45
36      cyan         ciano        46
37      grey          cinza       47
97      white        branco       107"""
#site para mudar o fundo do tkinter e mudar fundo de outras coisas
#https://treinamento24.com/library/lecture/read/735507-como-mudar-a-cor-de-fundo-do-python

#para adicionar mais cores haverá de usar uma biblioteca especifica


"""def main():
    root = Tk()   
    root.geometry('300x100')
    root.configure(background = 'black')
    app = Application(root)
    root.mainloop()  """
