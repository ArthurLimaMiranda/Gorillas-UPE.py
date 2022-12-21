import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle
from asciimatics.screen import Screen
from random import randint
import time, math, ctypes, frames, abertura


def telaCheia():
    kernel32 = ctypes.WinDLL('kernel32')
    user32 = ctypes.WinDLL('user32')
    SW_MAXIMIZE = 3
    hWnd = kernel32.GetConsoleWindow()
    user32.ShowWindow(hWnd, SW_MAXIMIZE)

def enter_is_terminate(x):
    if x == 10:
        x = 7
    return x

def score(window, pM1, p1Name, p1Score, pM2, p2Name, p2Score, width, height):
    score = str(p1Score)+" VS "+str(p2Score)
    rectangle(window,height-3,0,height-1,width-8)
    window.addstr(height-2, pM1[1],p1Name,curses.A_BOLD)
    window.addstr(height-2, pM2[1]+3,p2Name,curses.A_BOLD)
    window.addstr(height-2, int(width/2)-5, score,curses.A_STANDOUT)

def criaJanela(window, texto1, texto2, startRecX,finalRecX,stringX,finalUnidadeX):
    rectangle(window,1,startRecX,4,finalRecX)
    window.addstr(2,stringX,texto1)
    window.addstr(3,stringX,texto2)
    e1 = curses.newwin(1,4,2,finalUnidadeX)
    window.refresh()
    box = Textbox(e1)
    box.edit(enter_is_terminate)
    return box.gather()

def entrada(macaco, window, width):

    if (macaco == 1):
        startRecX = 1
        finalRecX = 20
        stringX = 2
        finalAnguloX = 10
        finalVelocidadeX = 14
    else:
        startRecX = width-20
        finalRecX = width-2
        stringX = width-19
        finalAnguloX = width-11
        finalVelocidadeX = width-7

    sair = False
    while(not sair):
        NAN=False
        angulo = criaJanela(window,'Angulo:','0->80º',startRecX,finalRecX,stringX,finalAnguloX) 
        try:
            int(angulo)
        except:
            NAN=True

        if((not NAN) and int(angulo)>=0 and int(angulo)<=80):
            sair=True
        else:
            sair=False

    sair = False
    while(not sair):
        NAN = False
        velocidade = criaJanela(window,'Velocidade:','3->15m/s',startRecX,finalRecX,stringX,finalVelocidadeX)
        try:
            int(velocidade)
        except:
            NAN=True

        if((not NAN) and int(velocidade)>=3 and int(velocidade)<=15):
            sair=True

        else:
            sair=False

    return int(angulo), int(velocidade)

def atualizar(sprite, frame, yFinal, xFinal):

    if ((frame == 0) or (frame == 2)):
        tamanhoJanela = 49
        yInicial = 5
    else:
        tamanhoJanela = 39
        yInicial = 4
        yFinal+=1

    janela = curses.newwin(yInicial,10, yFinal, xFinal)
    for i in range(tamanhoJanela):
        janela.refresh()
        janela.addstr(sprite[frame][i])

def criarPredio(altura):
    teto = ["@@@@@@@@@@@@@@@@"]
    corpo = ["@@@%%%%%%%%%%@@@"] * altura
    predio = teto + corpo
    return predio

def predioMacaco(macaco, alturaPredio, alturaTela, larguraTela):
    pM = randint(1,2)

    if(pM == 1):
        if (macaco==1):
            xM = 3
            yM = alturaTela-alturaPredio[0]-7
        else:
            xM=larguraTela-21
            yM = alturaTela-alturaPredio[-1]-7

    else:
        if (macaco==1):
            xM = 19
            yM = alturaTela-alturaPredio[1]-7
        else:
            xM = larguraTela-38
            yM = alturaTela-alturaPredio[-2]-7    

    return yM, xM

def colisaoComPersonagem(posicaoMacaco, posicaoProjetil):
    if((posicaoProjetil[1] >= (posicaoMacaco[1]-1)) and (posicaoProjetil[1] <= (posicaoMacaco[1]+9))):
        if((posicaoProjetil[0] <= posicaoMacaco[0]+5) and (posicaoProjetil[0] >= posicaoMacaco[0])):
            return True         
    else:
        return False   
    
def main(stdscr):

    stdscr.notimeout(True)
    height,width = stdscr.getmaxyx()
    
    p1Name = "MeuNome"
    p2Name = "Bot"
    p1Score = 0
    p2Score = 0
    gravidade = 0.98 ####Manualizar

    Screen.wrapper(abertura.demo)

    fim = False
    while not fim:

        live = False
        newShot = True
        shot = False
        macaco = randint(0,1)
        frameM1 = 0
        frameM2 = 0
        fps = 0

        #Geração de prédios com alturas aleatórias
        altura = [None] * 10
        predio = [None] * 10
        for i in range(10):
            altura[i] = randint(6,25)
        for i in range(10):
            predio[i] = criarPredio(altura[i])

        #Geração da posição dos macacos
        pM1 = predioMacaco(1,altura, height, width)
        pM2 = predioMacaco(2,altura, height, width)

        reset = False
        while not reset:
            stdscr.clear()
            stdscr.refresh()

            #Printa os prédios na tela
            for nPredio in range(10):
                for h in range(altura[nPredio]):
                    stdscr.refresh()
                    stdscr.addstr(height-altura[nPredio]+h-2, 0+(nPredio*17), predio[nPredio][h])
            stdscr.refresh()
            score(stdscr, pM1, p1Name, p1Score, pM2, p2Name, p2Score, width, height)

            #Printa os macacos na tela
            fps+=1
            if(shot):
                if(macaco == 1):
                    frameM1 = 2
                else:
                    frameM2 = 2
                fps = 0
                shot = False

            if(fps == 5):
                if(frameM1 == 2):
                    frameM1 = 0
                if(frameM2 == 2):
                    frameM2 = 0
                frameM1 = 1-frameM1
                frameM2 = 1-frameM2
                fps = 0

            atualizar(frames.macaco_Player1, frameM1, pM1[0], pM1[1])
            atualizar(frames.macaco_Player2, frameM2, pM2[0], pM2[1])
            
            if (live == True):
                stdscr.notimeout(False)
                stdscr.timeout(95) 
                x+=1
            if(newShot == True):
                angulo, v0 = entrada(macaco, stdscr, width)
                x = 0
                live = True
                shot = True
            
            if(macaco == 1):
                v0x = v0*math.cos(math.radians(angulo))
                t = math.tan(math.radians(angulo))  
                x0 = (pM1[1]+10)
                posX = int(x0 + x)
                y0 = (pM1[0]-1)   

            else:
                v0x = v0*math.cos(math.radians(180-angulo))
                t = math.tan(math.radians(180-angulo))
                x0 = (pM2[1])
                posX = int(x0 - x)
                y0 = (pM2[0]-1) 

            dX = (posX-x0)  
            a = (dX*t) - ((gravidade/2)*((dX/v0x)**2))  
            posY = int(y0 - a)
                
            pP= [posY, posX]
            newShot = False

            #Colisao entre projétil e prédio
            height-altura[nPredio]+h-2
            for i in range(10):
                if(((pP[1] >= ((i*17))) and (pP[1] <= (i*17)+15)) and (pP[0] >= (height-2-altura[i]))):
                    intervalo = list(predio[i][height-pP[0]-2-altura[i]])
                    intervalo[pP[1]-(i*17)] = ' '
                    predio[i][-1-(height-2-pP[0])] = ''.join(intervalo)
                    stdscr.notimeout(True)
                    live = False
                    newShot = True
                    macaco = 1-macaco

            if((pP[0]>0) and (pP[1]<width) and (pP[1]>0) and live):
                stdscr.addstr(pP[0], pP[1], '0')  
            elif(pP[0]<0 and (pP[1]<width) and (pP[1]>0)):
                stdscr.addstr(1, pP[1], "^")
            elif (((pP[1]>width) or (pP[1]<0)) and live):
                live = False
                newShot = True
                macaco = 1-macaco

            #Colisão entre projétil e personagem
            if(colisaoComPersonagem(pM1, pP)):
                reset = True
                p2Score = p2Score+1
                macaco = 1
            if(colisaoComPersonagem(pM2, pP)):
                reset = True
                p1Score = p1Score+1 
                macaco = 0   

            event = stdscr.getch()
            if event == 27:
                reset = True
                fim = True
                 
telaCheia()      
wrapper(main)