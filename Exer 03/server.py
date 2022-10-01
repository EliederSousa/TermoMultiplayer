import socket, threading, pickle, random, time
import fsm

MAX_CLIENTS     = 2
DEFAULT_PORT    = 30000
DEBUGMODE       = True

palavrasValidas = ["termo","suíte","ávido","festa","bebia","honra","ouvir","pesco","fungo","pagam","ginga", \
    "pinta","poder","útero","pilha","sarar","fruta","piano","notar","musgo","tensa","melão","feliz","miojo",\
    "pagos","texto","mamãe","ameno","chuva","coral","forte","tonta","temor","ligar","rolar","navio","limbo",\
    "calvo","fedor","balde","oxalá","talco","lábia","crime","grade","carta","flora","comum","fatal","pecar",\
    "feroz","vírus","armar","couro","êxito","ecoar","balão","falir","tecer","arena","justo","árido","ruiva",\
    "múmia","fogão","dupla","touca","sogro","ósseo","treta","átomo","sadio","cólon","pátio","molas","certo",\
    "risco","bossa","porre","tigre","vocal","treze","sueco","verbo","latim","povos","longo","lotar","depor",\
    "cento","trava","latão","ditos","tórax","polir","cacos","túnel","lindo","pegar","pilar","passo","piada",\
    "puxar","taças","manta","barba","subir","tosse","adega","veias","mesma","mirim","mansa","nobre","grama",\
    "ritmo","samba","ardor","daqui","bravo","surfe","tanto","imune","lucro","finos","bocas","toldo","major",\
    "cabos","estar","focal","ações","queda","juros","elite","burro","fundo","duelo","breve","bolso","linha",\
    "parir","furar","quina","pasta","suíno","dosar","cervo","sujar","corda","macia","reler","musas","verme",\
    "focar","maçãs","noção","anual","aérea","cerco","sócio","porca","fraco","punho","acima","varão","bolha",\
    "tanga","globo","rampa","goela","reais","cheio","fosso","pouco","danos","salas","mimar","sanha","óxido",\
    "suave","época","antro","total","jóias","polvo","jejum","atriz","recuo","ágeis","trenó","fluir","muito",\
    "ópera","ficar","bucha","magro","frota","série","ácido","ápice","líder","idoso","multa","primo","garça",\
    "banal","juíza","jorro","sismo","mercê","pônei","etapa","modas","colar","muita","papel","ruela","meias",\
    "gripe","causa","menor","nulos","caule","rubor","optar","redor","nação","galho","roubo","parto","cenas",\
    "pódio","lesar","telão","reúso","odiar","usual","latir","altos","livre","vosso","geada","etnia","trevo",\
    "rezar","bucal","vetor","filho","miolo","ordem","valor","filha","antes","vetar","surra","prata","ceder",\
    "pirão","frear","quilo","rombo","lomba","praia","urnas","aveia","picar","arcar","única","mágoa","jaula",\
    "gerar","trena","gemer","riste","lábio","busto","visar","velha","aéreo","adaga","crase","feras","missa",\
    "cobra","idéia","briga","dardo","berço","palmo","ralar","reles","blusa","super","grata","longa","tarso",\
    "vulto","lenda","grego","pinos","flúor","obeso","sauna","assim","troco","úteis","infra","pudor","cofre",\
    "prece","junho","manco","pisar","posse","copas","ninfa","gruta","regra","citar","mural","gíria","ruína",\
    "fases","faraó","míope","mando","frios","gelar","chave","sobra","opaco","lagos","corpo","doses","basco",\
    "caída","vinda","sujos","igual","lápis","julho","acaso","dados","favor","pente","beata","chulo","rumos",\
    "cubos","tento","toque","polpa","ombro","raras","pneus","canil","funil","perto","coala","amplo","orgia",\
    "doces","sobre","tédio","pinça","motel","trufa","voraz","azedo","coeso","ácaro","calmo","enfim","mitos",\
    "feios","palha","andar","crepe","pingo","avelã","malte","saída","monge","salto","lótus","rímel","lauda",\
    "damas","sadia","truco","sério","oeste","selva","reter","bolsa","anexo","renda","lobos","vício","zebra",\
    "modos","praxe","pudim","birra","praça","pedra","olhar","pizza","banho","bucho","afins","maior","cabra",\
    "visão","irado","razão","macio","troca","salmo","casta","mídia","trupe","morna","falso","lidar","afeto",\
    "verso","belos","páreo","vídeo","denso","herói","moeda","vaiar","cópia","coçar","aulas","ganho","chapa",\
    "jarra","velho","grilo","sigma","farsa","sigla","clone","cesta","anjos","rugir","luzes","árdua","parvo",\
    "censo","virar","apito","gosto","casto","fraca","agudo","sovar","fatos","torso","tumba","veste","leões",\
    "secar","berro","sutis","bispo","loção","pesar","digno","bamba","broca","hiato","clube","totem","prumo",\
    "meios","vulgo","esqui","épico","minha","ainda","remar","manso","ousar","viral","óvulo","trote","artes",\
    "facas","brava","meiga","campo","levar","preta","lebre","pobre","gesso","sabiá","freio","marte","clara",\
    "magos","reino","murro","calar","prosa","feita","folga","terço","patas","vogal","zíper","divas","borda",\
    "penar","errar","névoa","morto","forma","áureo","vapor","circo","faixa","beijo","bufão","pedir","tropa",\
    "vital","vento","cárie","vespa","negro","pardo","local","beato","quais","frase","sucos","botão","balsa",\
    "foice","nozes","dente","cedro","aceno","repor","leque","drama","forno","tarde","sarro","certa","trama",\
    "milho","dreno","carma","poeta","máfia","lenço","nunca","ficha","ótica","molho","barão","cútis","toada",\
    "trens","chalé","ciclo","leigo","golpe","haver","varal","ritos","fibra","nervo","irmãs","sagaz","gente",\
    "pombo","zinco","pavor","feixe","pular","titia","deter","axila","brejo","rever","naipe","arder","então",\
    "pleno","parma","juízo","noite","seiva","furor","janta","mover","vidro","votar","pilha","brasa","areal",\
    "jarro","poços","ninja","nossa","boiar","outra","pires","regar","boato","sumir","lenta","loira","cinza",\
    "fisco","agora","lazer","pista","pulga","fosca","males","conto","tocha","retas","cuspe","persa","gêmeo",\
    "tenda","águia","meros","robôs","lados","areia","impor","vigor","médio","matiz","órgão","senso","novas",\
    "turco","densa","balas","bicho","galão","atual","monte","tribo","tarda","baita","ampla","floco","banjo",\
    "olhos","gasto","fácil","acesa","torto","horta","alçar","vivos","gaita","solto","cetro","redes","criar",\
    "sacro","banir","prato","gorro","miúdo","moída","aliar","bater","fauna","norte","haste","alado","bloco",\
    "pinga","ético","corja","morno","ideal","fusão","verão","vozes","bílis","ímpar","sogra","jovem","testa",\
    "metal","falsa","bruto","tenso","dique","fator","sutil","grupo","matar","motor","meses","vazio","cujos",\
    "parda","carpa","árabe","plebe","advir","punir","rival","trave","tricô","lento","sarda","gozar","caber",\
    "sexta","sacra","rolha","açude","casos","cisão","chata","ossos","expor","venda","casco","banco","bomba",\
    "sinal","horto","ramos","fonte","leito","cobre","tíbia","cinco","noiva","ponto","aluno","traje","canal",\
    "rouco","boate","mútuo","caros","lente","lares","sacar","porém","feudo","vezes","carga","invés","presa",\
    "geral","negar","atuar","ciúme","fiado","força","corvo","gordo","tutor","duros","exame","caldo","cupim",\
    "ótimo","mamar","índio","autos","pavio","fobia","jeito","votos","tesão","lagoa","pampa","diodo","parte",\
    "ambas","farda","sonar","bacon","gatas","banca","meigo","pavão","fixos","doido","valer","girar","fofas",\
    "caspa","opção","macro","prego","perda","enjoo","longe","ícone","ferro","braço","unida","lição","roçar",\
    "bambu","dorso","moral","ameba","viril","amora","magna","rural","penal","abuso","sunga","poção","erros",\
    "surda","beber","cifra","móvel","atrás","farol","fugaz","zerar","menta","estes","vênus","vista","final",\
    "nevar","norma","leste","nudez","telas","tinto","saber","bingo","cacau","fardo","morar","bioma","domar",\
    "grega","coice","ervas","medir","mista","atroz","raios","tosar","muros","santa","desde","posto","cesto",\
    "abril","penta","celta","mudar","cacho","bando","caixa","resto","libra","régua","calda","preto","tênue",\
    "vazar","reger","usina","vazia","todos","durar","rimar","angra","selos","aliás","preço","bufar","nuvem",\
    "ética","lapso","união","civis","grito","bônus","cinto","matos","safra","algoz","letra","dogma","pesca",\
    "linho","tchau","graxa","casal","lidos","zonas","lorde","larva","gnomo","casca","botar","tinta","prado",\
    "ânimo","bacia","magia","saque","grato","bares","rolos","loura","óbvio","viola","linda","sábio","cueca",\
    "santo","couve","susto","ostra","altar","fúria","limpo","trair","ídolo","deusa","usura","caçar","todas",\
    "obter","tampa","fossa","lavar","gueto","lunar","panda","vácuo","rigor","humor","pulso","terno","anéis",\
    "donos","coxão","civil","bocal","aroma","soldo","morro","coxas","cupom","jogos","furos","arcos","louca",\
    "peste","crise","homem","duplo","táxis","pauta","canja","cauda","dizer","rapaz","atlas","jogar","sítio",\
    "guiar","babar","trono","trigo","novos","massa","horas","junto","ômega","salsa","pinho","brisa","ambos",\
    "guria","brega","motim","rumor","sutiã","ducha","misto","farto","pólen","débil","dicas","canto","cargo",\
    "seita","graus","baile","zelar","apelo","arroz","canoa","perna","tarja","vasos","fluxo","falar","dobro",\
    "órfão","leite","curso","comer","cisne","fêmea","cheia","lugar","prazo","letal","seção","fiapo","vinte",\
    "puxão","revés","clipe","tomar","manto","gesto","praga","áudio","ânsia","tripé","licor","álibi","inato",\
    "lance","rédea","mútua","vagão","lesma","beira","abono","salão","russo","caqui","pelos","servo","facão",\
    "barro","filme","rouca","nisto","corar","idade","lisos","selim","peixe","untar","sanar","grana","panos",\
    "relva","plena","besta","banda","sódio","feira","pompa","veloz","belas","poema","tecla","adeus","dobra",\
    "fruto","sorte","sabão","sushi","quibe","corno","tênis","tosco","valsa","lacre","fosco","neném","clero",\
    "dever","dúzia","ração","terça","sótão","fuzuê","aviso","prole","costa","manga","metro","pirar","verde",\
    "único","vacas","suado","fixar","loiro","fogos","dunas","radar","baixa","frevo","terra","calva","harpa",\
    "dueto","prova","pluma","irmão","justa","pagar","farpa","cerca","vôlei","rosca","euros","curar","fenda",\
    "farra","áreas","unhas","nomes","tábua","gosma","capuz","ileso","lenha","perua","padre","fazer","tocar",\
    "bruxo","lojas","lerdo","nisso","golfo","topar","usada","ruivo","saúde","nadar","lixar","vidas","pomba",\
    "êxodo","acolá","dotar","raiar","batom","ontem","torpe","oásis","cloro","curva","surto","ricos","ursos",\
    "hiena","vasta","risos","febre","fumar","fórum","lutar","catar","trela","litro","surdo","menos","choro",\
    "chefe","vasto","cetim","traço","cílio","extra","greve","tapar","tufão","sarau","rosas","touro","trapo",\
    "lírio","abano","delta","cação","anzol","sarna","clave","refém","hífen","claro","nasal","burra","conde",\
    "ponte","ondas","quota","mexer","verba","aonde","obras","idosa","signo","frias","lesão","mundo","gênio",\
    "legal","tempo","âmbar","culta","vinho","livro","ninho","germe","culto","pasto","podre","mirar","teses",\
    "ébrio","naves","afago","laudo","ditar","selar","garra","folia","pedal","ninar","tirar","fugir","calor",\
    "naval","porta","âmago","ponta","calma","capaz","genro","almas","feias","senão","barco","zonzo","senha",\
    "focos","óssea","rosto","socar","carne","garfo","luvas","chiar","vazão","porco","gases","úmido","boina",\
    "laços","ferir","média","roupa","duque","bonde","tiros","avaro","exato","dócil","basta","viver","placa",\
    "disso","poros","arame","outro","sopas","ótima","bruxa","raiva","museu","astro","rente","lombo","bordo",\
    "cinta","manhã","palco","peões","folha","treco","casar","louco","turvo","rádio","tipos","somar","achar",\
    "macho","ajuda","times","meter","graça","mosca","milha","carro","algum","conta","nicho","sabor","natal",\
    "tátil","cerne","torta","apoio","símio","fetal","hotel","setor","vesgo","amada","firma","hábil","calça",\
    "aspas","latas","quase","creme","telha","teias","assar","lousa","baque","rubro","fotos","adiar","dólar",\
    "polar","limão","lança","coroa","pomar","tripa","mesmo","jegue","álbum","custo","fútil","laico","dedos",\
    "ganso","visor","abrir","dedão","bazar","gerir","mania","rodar","turno","anões","sexto","palma","parco",\
    "pouso","moela","ótico","áries","tenor","amido","solar","poste","urubu","coisa","seara","xampu","dieta",\
    "rocha","turma","paiol","vilão","nível","pouca","vinil","frade","tonto","cavar","lilás","nariz","torre",\
    "parar","supor","gambá","cravo","árduo","tosca","clima","sósia","chato","moita","vagar","pausa","truta",\
    "podar","fuçar","posar","autor","cruel","quiçá","avião","retro","dores","credo","hinos","capim","tango",\
    "vocês","jurar"]

#clientes = {}
#numClientes = 0

"""
esperarClientes ==> gameloop ==> wait
                       /\         ||
                       ||         ||
                       \\=========//  """

fsm = fsm.FiniteStateMachine()
fsm.createState("esperarclientes",["gameloop"])
fsm.createState("gameloop", ["wait"])
fsm.createState("wait", ["gameloop"])
fsm.changeState("esperarclientes")

# nome, addr, info, text
class ClienteInfo:
    nome = ""
    addr = ""
    info = ""
    text = ""

# info, code, seg
class ServerInfo:
    info = ""
    code = ""

class GameLogic:
    global fsm
    state = fsm
    word = "TESTE"
    seg = 0
    winner = ""
    clientes = {}
    numClientes = 0
    numClientesParaIniciar = 1

logic = GameLogic()

print("\n \
  ________________  __  _______  _____ __________ _    ____________  \n \
 /_  __/ ____/ __ \/  |/  / __ \/ ___// ____/ __ \ |  / / ____/ __ \ \n \
  / / / __/ / /_/ / /|_/ / / / /\__ \/ __/ / /_/ / | / / __/ / /_/ / \n \
 / / / /___/ _, _/ /  / / /_/ /___/ / /___/ _, _/| |/ / /___/ _, _/  \n \
/_/ /_____/_/ |_/_/  /_/\____//____/_____/_/ |_| |___/_____/_/ |_|   \n \
")
print("             Proudly created by Elieder & Jose Team\n")

"""Retorna o IP local do host.
Returns:
    str: O número de IP associado à NIC na interface local.
"""
def getMyIP():
    ip = socket.gethostbyname(socket.gethostname())
    print("IP local:", ip)
    return ip

"""Abre um socket para o servidor.
Args:
    str IP: O IP para usar ao criar o socket.
    int porta: O número da porta usada no socket.
Returns:
    socket: Um manipulador para o socket criado.
"""
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


serv = socketCreate(getMyIP(), DEFAULT_PORT)
serv.listen(MAX_CLIENTS)
print("Servidor ouvindo a porta {}.".format(DEFAULT_PORT))


def broadcast( serverInfoObject ):
    global logic
    for w in logic.clientes:
        try:
            logic.clientes[w]["socket"].send(pickle.dumps(serverInfoObject))
        except:
            print("Erro ao dar broadcast.")


def gameLogicThread():
    global logic
    svinfo = ServerInfo()
    serverTicks = 0
    while True:
        serverTicks += 1
        if serverTicks > 2**31:
            serverTicks = 0
        #if (serverTicks % 20000000 == 0):
        #    print(logic.state.getState())
        if logic.state.getState() == "esperarclientes":
            if logic.numClientes == logic.numClientesParaIniciar:
                logic.state.changeState("gameloop")
                logic.word = palavrasValidas[random.randrange(0, len(palavrasValidas))].upper()
                print("\nIniciando uma nova rodada, palavra alvo: {}".format(logic.word))
                svinfo.code = 200
                svinfo.info = "gameloop"
                broadcast(svinfo)
            else:
                svinfo.code = 200
                svinfo.info = "Esperando por mais {} jogadores.".format(logic.numClientesParaIniciar - logic.numClientes)
                broadcast(svinfo)
        elif logic.state.getState() == "gameloop":
            pass
        elif logic.state.getState() == "wait":
            time.sleep(1)
            if logic.seg > 0:
                if logic.seg == 4:
                    print("{} ganhou.".format(logic.winner))
                print("Nova rodada em {}s".format(logic.seg))
                logic.seg -= 1
                svinfo.info = "{} ganhou.\nNova rodada em {}s\n".format(logic.winner, logic.seg)
                svinfo.code = 910
                broadcast( svinfo )
            else:
                logic.state.changeState("gameloop")
                logic.word = palavrasValidas[random.randrange(0, len(palavrasValidas))].upper()
                print("\nIniciando uma nova rodada, palavra alvo: {}".format(logic.word))
                logic.seg = 5
                svinfo.info = "gameloop"
                svinfo.code = 200
                broadcast( svinfo )


def checarPalavra( palavra ):
    global logic
    palavra = palavra.upper()
    palavraCopia = logic.word
    resultado = ""
    for w in range( 5 ):
        if palavra[w] == logic.word[w]:
            resultado += "c"  # Letra Certa (posição certa)
        else:
            index = palavraCopia.find(palavra[w])
            if index > -1:
                resultado += "q"  # Letra Quase certa (posição errada)
                palavraCopia = palavraCopia[0:index:] + palavraCopia[index+1::]
            else:
                resultado += "e"  # Letra Errada

    if resultado == "ccccc":
        return True, resultado
    else:
        return False, resultado


def clientThread( con, ipAddress, port):
    global logic
    svInfo = ServerInfo()

    while True:
        try:
            data = con.recv(2048)
            data = pickle.loads(data)
            if data:
                if data.info == "login":
                    temp = ServerInfo()
                    temp.code = 200
                    temp.info = "Conectado!"
                    con.send(pickle.dumps(temp))
                    print("\n================ NOVO CLIENTE ================")
                    print("Usuário: {}, {} : {}".format(data.nome, ipAddress, port))
                    print("Clientes online:", logic.numClientes)
                    logic.clientes[ipAddress]["nome"] = data.nome
                elif data.info == "gameloop":
                    print("{} enviou {}".format(data.nome, data.text))
                    teste, erros = checarPalavra( data.text )
                    if not teste:
                        temp.code = 900
                        temp.info = erros #c = letra certa, q = quase certa, e = letra errada
                        con.send(pickle.dumps(temp))
                    else:
                        logic.winner = data.nome
                        logic.clientes[ipAddress]["pontuacao"] += 1
                        logic.seg = 5
                        logic.state.changeState("wait")

            else:
                print("Cliente no IP {} não enviou dados".format(con))
                break

        except socket.error as e:
            print(e)
            break

    logic.numClientes -= 1
    print("Clientes online:", logic.numClientes)
      

threading.Thread(target=gameLogicThread).start()

running = True
while running:
    sock, addr = serv.accept()

    if addr[0] in logic.clientes and not DEBUGMODE:
        print("IP {} chutado por tentar se conectar novamente.".format(addr[0]))
        temp = ServerInfo()
        temp.code = 404
        sock.send(pickle.dumps(temp))
    elif logic.numClientes == MAX_CLIENTS:
        temp = ServerInfo()
        temp.code = 502
        sock.send(pickle.dumps(temp))
    else:
        logic.clientes[addr[0]] = {}
        logic.clientes[addr[0]]["socket"] = sock
        logic.clientes[addr[0]]["pontuacao"] = 0
        logic.numClientes += 1
        thread = threading.Thread(target=clientThread, args=(sock, addr[0], addr[1])).start()
