import curses
from curses import KEY_ENTER, KEY_DOWN, KEY_UP, wrapper
from curses.textpad import Textbox, rectangle
from random import randint
import time, math, ctypes 
import funcoes, frames
            
gorillasInfo1 = """
Gorillas é um jogo onde o principal objetivo é 
atingir o macaco adversário com um explosivo.
"""

gorillasInfo2 = """
O explosivo é atirado com base em um ângulo 
e uma velocidade inseridos pelo usuário. O 
vencedor é   
"""
gorillasInfo3="""
escolhido dentre quem ganhar mais rodadas.
"""

gorillasInfo4 = """
     Esta versão do jogo possui 4 níveis de dificuldade:
     0 -> Dificuldade padrão, sem adesão de dificuldade;
     1 -> Caso ativa, o tiro terá um tempo limite de existência antes de se auto destruir;
     2 -> Se esta dificuldade for escolhida, a cada 3 tiros um novo cenário será gerado.
     3 -> Se esta dificuldade for escolhida, havera a chance do tiro destruir mais de um 
          bloco quando cair de cima.

     *Todas as dificuldades podem estar ativas ao mesmo tempo
"""

nome1=""
nome2=""
gravidade=""
rodadas=""
desafios="Ex: 0123"
check=False


def menu(stdscr):
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_YELLOW)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_MAGENTA)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_CYAN)

    height,width = stdscr.getmaxyx()
    stdscr.notimeout(False)
    stdscr.timeout(600)

    linha = 0
    linhaMax = 0
    frameM1 = 0
    frameM2 = 0
    fps = 0

    menuInicial = True
    menuNewGame = False
    manuInformacoes = False
    menuRanking = False

    altura = [None] * 10
    predio = [None] * 10
    for i in range(10):
        altura[i] = randint(6,25)
    for i in range(10):
        predio[i] = funcoes.criarPredio(altura[i])

    pM1 = funcoes.predioMacaco(1,altura, height, width)
    pM2 = funcoes.predioMacaco(2,altura, height, width)

    while True:
        curses.curs_set(0)
        stdscr.clear()
        rectangle(stdscr,1,2,height-2,width-1)
        stdscr.refresh()
        janelaBackGround = curses.newwin(height-4,width-4,2,3)
        janelaBackGround.clear()
        janelaBackGround.bkgd(' ', curses.color_pair(2) | curses.A_BOLD)
        janelaBackGround.refresh()

        for nPredio in range(10):
            for h in range(altura[nPredio]):
                stdscr.refresh()
                stdscr.addstr(height-altura[nPredio]+h-2, 5+(nPredio*17), predio[nPredio][h])
        
        fps+=1
        if(fps == 1):
            if(frameM1 == 2):
                frameM1 = 0
            if(frameM2 == 2):
                frameM2 = 0
            frameM1 = 1-frameM1
            frameM2 = 1-frameM2
            fps = 0

        
        funcoes.atualizar(frames.macaco_Player1, frameM1, pM1[0], pM1[1], True)
        funcoes.atualizar(frames.macaco_Player2, frameM2, pM2[0], pM2[1], True)

        if(menuInicial):
            linhaMax = 3      
            rectangle(stdscr,1,int(width/2)-10,height-2,int(width/2)+10)
        
            stdscr.refresh()
            janelaInici = curses.newwin(height-4,19,2,int(width/2)-9)
            janelaInici.bkgd(' ', curses.color_pair(3) | curses.A_BOLD)
            janelaInici.clear()
            janelaInici.addstr(20,5,"Novo Jogo", curses.A_BLINK if linha==0 else curses.A_NORMAL)
            janelaInici.addstr(25,5,"Informações", curses.A_BLINK if linha==1 else curses.A_NORMAL)
            janelaInici.addstr(30,5,"Ranking", curses.A_BLINK if linha==2 else curses.A_NORMAL)
            janelaInici.addstr(35,5,"Sair", curses.A_BLINK if linha==3 else curses.A_NORMAL)
            janelaInici.addstr(20+(linha*5), 1,"-->")
            janelaInici.refresh()
            event = stdscr.getch()
            if (event == 10):
                if (linha==0):
                    menuInicial = False
                    menuNewGame = True
                    nome1=""
                    nome2=""
                    gravidade=""
                    rodadas=""
                    desafios="Ex: 012"
                    check=False

                if (linha==1):
                    menuInicial = False
                    manuInformacoes = True
                    stdscr.clear()
                if (linha==2):
                    menuInicial = False
                    menuRanking = True
                if (linha==3):
                    return False
        elif(menuNewGame):
            linhaMax = 6           

            rectangle(stdscr,1,11,height-2,28)
            rectangle(stdscr,17,28,height-13,139)

            stdscr.refresh()    
            janelaInfo1 = curses.newwin(height-4,16,2,12)
            janelaInfo1.clear()
            janelaInfo1.bkgd(' ', curses.color_pair(3) | curses.A_BOLD)
            janelaInfo1.addstr(21, 3,"Novo Jogo",curses.A_BLINK)
            janelaInfo1.addstr(23, 3,"Informações",curses.A_ITALIC)
            janelaInfo1.addstr(25, 3,"Ranking",curses.A_ITALIC)
            janelaInfo1.addstr(27, 3,"Sair",curses.A_ITALIC)
            janelaInfo1.refresh()

            
            janelaInfo2 = curses.newwin(23,110,18,29)
            janelaInfo2.clear()
            janelaInfo2.bkgd(' ', curses.color_pair(4) | curses.A_BOLD)

            rectangle(janelaInfo2,1,20,3,31)
            janelaInfo2.addstr(2,4,"Nome do player1:",curses.A_UNDERLINE if linha==0 else curses.A_BLINK)
            janelaInfo2.addstr(2,21,nome1,curses.A_BOLD)
            rectangle(janelaInfo2,4,20,6,31)
            janelaInfo2.addstr(5,4,"Nome do player2:",curses.A_UNDERLINE if linha==1 else curses.A_BLINK)
            janelaInfo2.addstr(5,21,nome2,curses.A_BOLD)
            rectangle(janelaInfo2,7,30,9,35)
            janelaInfo2.addstr(8,4,"Valor da gravidade (1-10):",curses.A_UNDERLINE if linha==2 else curses.A_BLINK)
            janelaInfo2.addstr(8,31,gravidade,curses.A_BOLD)
            rectangle(janelaInfo2,10,12,12,16)
            janelaInfo2.addstr(11,4,"Rodadas:",curses.A_UNDERLINE if linha==3 else curses.A_BLINK)
            janelaInfo2.addstr(11,13,rodadas,curses.A_BOLD)
            rectangle(janelaInfo2,13,47,15,57)
            janelaInfo2.addstr(14,4,"Desafios (detalhes no menu de informações):",curses.A_UNDERLINE if linha==4 else curses.A_BLINK)
            janelaInfo2.addstr(14,48,desafios,curses.A_BOLD)

            janelaInfo2.addstr(17,50,"Enviar",curses.A_BLINK if linha==5 else curses.A_NORMAL)
            janelaInfo2.addstr(20,50,"Retornar",curses.A_BLINK if linha==6 else curses.A_NORMAL)

            janelaInfo2.addstr(2+(linha*3), 60,"<--")
            janelaInfo2.refresh()

            event = stdscr.getch()
            if (event == 10):
                if(linha==0):
                    e1 = curses.newwin(1,10,20,50)
                    janelaInfo2.refresh()
                    box = Textbox(e1)
                    box.edit(funcoes.enter_is_terminate)
                    nome1
                    nome1 = box.gather()

                elif(linha==1):
                    e1 = curses.newwin(1,10,23,50)
                    janelaInfo2.refresh()
                    box = Textbox(e1)
                    box.edit(funcoes.enter_is_terminate)
                    nome2
                    nome2 = box.gather()

                elif(linha==2):
                    sair = False
                    while(not sair):
                        NAN=False
                        e1 = curses.newwin(1,4,26,60)
                        janelaInfo2.refresh()
                        box = Textbox(e1)
                        box.edit(funcoes.enter_is_terminate)
                        gravidade
                        gravidade = box.gather() 
                        try:
                            float(gravidade)
                        except:
                            NAN=True

                        if((not NAN) and float(gravidade)>=1 and float(gravidade)<=10):
                            sair=True
                        else:
                            sair=False

                elif(linha==3):
                    sair = False
                    while(not sair):
                        NAN=False
                        e1 = curses.newwin(1,3,29,42)
                        janelaInfo2.refresh()
                        box = Textbox(e1)
                        box.edit(funcoes.enter_is_terminate)
                        rodadas
                        rodadas = box.gather()
                        try:
                            int(rodadas)
                        except:
                            NAN=True

                        if((not NAN) and int(rodadas)>=1):
                            sair=True
                        else:
                            sair=False

                elif(linha==4):
                    sair = False
                    while(not sair):
                        NAN=False
                        e1 = curses.newwin(1,9,32,77)
                        janelaInfo2.refresh()
                        box = Textbox(e1)
                        box.edit(funcoes.enter_is_terminate)
                        desafios
                        desafios = box.gather()
                        try:
                            int(desafios)
                        except:
                            NAN=True

                        if((not NAN) and int(desafios)>=0):
                            sair=True
                            check=True
                        else:
                            sair=False

                elif(linha==5):
                    if(nome1!=''and nome2!=''and gravidade!=''and rodadas!=''and check):
                        return nome1, nome2, gravidade, rodadas, desafios

                elif(linha==6):
                    menuInicial = True
                    menuNewGame = False
                    linha = 0

        elif(manuInformacoes):
            linhaMax = 0           

            rectangle(stdscr,1,11,height-2,28)
            rectangle(stdscr,17,28,height-13,139)

            stdscr.refresh()    
            janelaInfo1 = curses.newwin(height-4,16,2,12)
            janelaInfo1.clear()
            janelaInfo1.bkgd(' ', curses.color_pair(3) | curses.A_BOLD)
            janelaInfo1.addstr(21, 3,"Novo Jogo",curses.A_ITALIC)
            janelaInfo1.addstr(23, 3,"Informações",curses.A_BLINK)
            janelaInfo1.addstr(25, 3,"Ranking",curses.A_ITALIC)
            janelaInfo1.addstr(27, 3,"Sair",curses.A_ITALIC)
            janelaInfo1.refresh()

            
            janelaInfo2 = curses.newwin(23,110,18,29)
            janelaInfo2.clear()
            janelaInfo2.bkgd(' ', curses.color_pair(4) | curses.A_BOLD)
            janelaInfo2.addstr(2,5,gorillasInfo1.replace("\n",""))
            janelaInfo2.addstr(5,5,gorillasInfo2.replace("\n",""))
            janelaInfo2.addstr(6,5,gorillasInfo3.replace("\n",""))
            janelaInfo2.addstr(9,18,gorillasInfo4)
            janelaInfo2.addstr(20,48,"Retornar", curses.A_BLINK)
            janelaInfo2.addstr(20,43,"-->")
            janelaInfo2.refresh()

            event = stdscr.getch()
            if (event == 10):
                menuInicial = True
                manuInformacoes = False
                linha = 0  
        elif(menuRanking):
            linhaMax = 0
            rectangle(stdscr,1,49,height-2,66)
            rectangle(stdscr,17,66,height-13,107)

            stdscr.refresh()    
            janelaInfo1 = curses.newwin(height-4,16,2,50)
            janelaInfo1.clear()
            janelaInfo1.bkgd(' ', curses.color_pair(3) | curses.A_BOLD)
            janelaInfo1.addstr(21, 3,"Novo Jogo",curses.A_ITALIC)
            janelaInfo1.addstr(23, 3,"Informações",curses.A_ITALIC)
            janelaInfo1.addstr(25, 3,"Ranking",curses.A_BLINK)
            janelaInfo1.addstr(27, 3,"Sair",curses.A_ITALIC)
            janelaInfo1.refresh()

            
            janelaInfo2 = curses.newwin(23,40,18,67)
            janelaInfo2.clear()
            janelaInfo2.bkgd(' ', curses.color_pair(4) | curses.A_BOLD)
            janelaInfo2.addstr(2,9,"Ranking de jogadores",curses.A_BLINK)

            ranking = funcoes.lerRanking()

            if(not ranking):
                janelaInfo2.addstr(10,3,"Ainda não há nenhuma classificação",curses.A_BOLD)
            else:
                tamanho = min(len(ranking[0]), 6)
                gorillasTop10 = "Lista das "+str(tamanho)+" melhores pontuações:"
                janelaInfo2.addstr(5,3,gorillasTop10,curses.A_BOLD)

                for x in range(tamanho):
                    texto = str(x+1)+"- "+str(ranking[0][x])+" com "+str(ranking[1][x])+" pontos"
                    janelaInfo2.addstr(8+(x*2),3,texto,curses.A_BOLD)

            janelaInfo2.addstr(21,16,"Retornar", curses.A_BLINK)
            janelaInfo2.addstr(21,12,"-->")
            janelaInfo2.refresh()
            janelaInfo2.refresh()

            event = stdscr.getch()
            if (event == 10):
                menuInicial = True
                menuRanking = False
                linha = 0

        if (event == 27):
                return False
        if (event == KEY_DOWN):
            linha+=1
            if (linha>linhaMax):
                linha=linhaMax
        if (event == KEY_UP):
            linha-=1
            if (linha<0):
                linha=0    