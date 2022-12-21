import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle
from random import randint
import time
import math
import ctypes


macaco1 = ["    __     ((****)) () (**) ()() (  ) ()   -  -   ",
           "    __     ((****)) () (  ) () @ -  -@  ",
           "  @        () __     ((****))    (  ) ()   -  -@    "]

macaco2 = ["    __     ((****)) () (**) ()() (  ) ()   -  -   ",
           "    __     ((****)) () (  ) () @ -  -@  ",
           "        @     __  () ((****)) () (  )    @ -  -  "]



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

def criaJanela(window, texto1, texto2, startRecX,finalRecX,stringX,finalUnidadeX):
    rectangle(window,1,startRecX,4,finalRecX)
    window.addstr(2,stringX,texto1)
    window.addstr(3,stringX,texto2)
    e1 = curses.newwin(1,4,2,finalUnidadeX)
    window.refresh()
    box = Textbox(e1)
    box.edit(enter_is_terminate)
    return box.gather()

def entrada(macaco, window, width, erro=False):

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
        NAN = False
        angulo = criaJanela(window,'Angulo:','0->80º',startRecX,finalRecX,stringX,finalAnguloX) 
        try:
            int(angulo)
        except:
            NAN = True

        if((not NAN) and int(angulo)>=0 and int(angulo)<=80):
            sair = True
        else:
            sair = False

    sair = False
    while(not sair):
        NAN = False
        velocidade = criaJanela(window,'Velocidade:','3->15m/s',startRecX,finalRecX,stringX,finalVelocidadeX)
        try:
            int(velocidade)
        except:
            NAN = True

        if((not NAN) and int(velocidade)>=3 and int(velocidade)<=15):
            sair = True

        else:
            sair = False

    return int(angulo), int(velocidade)

def atualizar(sprite, frame, yFinal, xFinal):

    if ((frame == 0) or (frame == 2)):
        tamanhoJanela = 49
        yInicial = 5
    else:
        tamanhoJanela = 39
        yInicial = 4
        yFinal = yFinal+1

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
            xM = 4
            yM = alturaTela - alturaPredio[0] - 5
        else:
            xM=larguraTela-21
            yM = alturaTela - alturaPredio[-1] - 5

    else:
        if (macaco==1):
            xM = 20
            yM = alturaTela - alturaPredio[1] - 5
        else:
            xM = larguraTela-38
            yM = alturaTela - alturaPredio[-2] - 5       

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
   
    macaco = randint(0,1)
    gravidade = 0.98 ####Manualizar
    frameM1 = 0
    frameM2 = 0
    fps = 0
    live = False
    newShot = True
    shot = False

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

    while True:
        stdscr.clear()
        stdscr.refresh()

        #Printa os prédios na tela
        for nPredio in range(10):
            for h in range(altura[nPredio]):
                stdscr.refresh()
                stdscr.addstr(height-altura[nPredio]+h, 0+(nPredio*17), predio[nPredio][h])

        #Printa os macacos na tela
        fps = fps+1

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

        atualizar(macaco1, frameM1, pM1[0], pM1[1])
        atualizar(macaco2, frameM2, pM2[0], pM2[1])
        
        
        if (live == True):
            stdscr.notimeout(False)
            stdscr.timeout(95) 
            x+=1

        if(newShot == True):
            macaco = 1-macaco
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

        if((pP[0]>0) and (pP[1]<width) and (pP[1]>0) and live):
            try: stdscr.addstr(pP[0], pP[1], '0')  
            except: 
                live = False
                newShot = True
            
        elif (((pP[1]>width) or (pP[1]<0)) and live):
            live = False
            newShot = True

        #Colisao entre projétil e prédio
        for i in range(9):
            if(((pP[1] >= ((i*17))) and (pP[1] <= (i*17)+15)) and (pP[0] >= (height-altura[i]))):
                intervalo = list(predio[i][height-pP[0]-altura[i]])
                intervalo[pP[1]-(i*17)] = ' '
                predio[i][-1-(height-pP[0])] = ''.join(intervalo)
                stdscr.notimeout(True)
                live = False
                newShot = True

        #Colisão entre projétil e personagem
        if(colisaoComPersonagem(pM1, pP)):
            break
        if(colisaoComPersonagem(pM2, pP)):
            break        

        event = stdscr.getch()
        if event == 27:
            break
                 
telaCheia()      
wrapper(main)