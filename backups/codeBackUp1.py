import math
import curses
from curses import wrapper,KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP
import time
from random import randint
import ctypes


macaco1 = "@@@@@@@@@@@%%%%%%%@@%%%%%%%@@%%%%%%%@@@@@@@@@@@@@@"
macaco2 = "@@@@@@@@@@@%%%%%%%@@%%%%%%%@@%%%%%%%@@@@@@@@@@@@@@"

def telaCheia():
    kernel32 = ctypes.WinDLL('kernel32')
    user32 = ctypes.WinDLL('user32')
    SW_MAXIMIZE = 3
    hWnd = kernel32.GetConsoleWindow()
    user32.ShowWindow(hWnd, SW_MAXIMIZE)

def atualizar(sprite, y, x):
    janela = curses.newwin(5,10, y, x)
    for i in range(49):
        janela.refresh()
        janela.addstr(sprite[i])

def criarPredio(altura):
    teto = ["@@@@@@@@@@@@@@@@"]
    corpo = ["@@@%%%%%%%%%%@@@"] * altura
    predio = teto + corpo
    return predio

def colisaoComPersonagem(posicaoMacaco, posicaoProjetil):
    if((posicaoProjetil[1] >= (posicaoMacaco[1]-1)) and (posicaoProjetil[1] <= (posicaoMacaco[1]+9))):
        if((posicaoProjetil[0] <= posicaoMacaco[0]+5) and (posicaoProjetil[0] >= posicaoMacaco[0])):
            return True         
    else:
        return False

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

def main(stdscr):

    stdscr.notimeout(True)
    height,width = stdscr.getmaxyx()
    gravidade = 0.98
    tempo = 0
    angulo = 15
    v0 = 10
    v0x = v0*math.cos(math.radians(angulo))
    v0y = v0*math.tan(math.radians(angulo))


    #Geração de prédios com alturas aleatórias
    altura = [None] * 10
    predio = [None] * 10
    for i in range(10):
        altura[i] = randint(5,25)
    for i in range(10):
        predio[i] = criarPredio(altura[i])

    #Geração da posição dos macacos
    pM1 = predioMacaco(1,altura, height, width)
    pM2 = predioMacaco(2,altura, height, width)

    live = False
    while True:
        stdscr.clear()
        stdscr.refresh()

        #Printa os prédios na tela
        for nPredio in range(10):
            for h in range(altura[nPredio]):
                stdscr.refresh()
                stdscr.addstr(height-altura[nPredio]+h, 0+(nPredio*17), predio[nPredio][h])

        #Printa os macacos na tela   
        atualizar(macaco1, pM1[0], pM1[1])
        atualizar(macaco2, pM2[0], pM2[1])
        
        if(live):
            tempo+=1

        a = v0y*tempo - ((gravidade/2)*tempo*tempo)         
        posX = int((pM1[1]+10) + (v0x*tempo))
        posY = int((pM1[0]-1) - a)


        pP = [posY,posX]

        #Colisao entre projétil e prédio
        for i in range(9):
            if(((pP[1] >= ((i*17))) and (pP[1] <= (i*17)+16)) and (pP[0] >= (height-altura[i]))):
                intervalo = list(predio[i][height-pP[0]-altura[i]])
                intervalo[pP[1]-(i*17)] = ' '
                predio[i][-1-(height-pP[0])] = ''.join(intervalo)
                stdscr.notimeout(True)
                live = False

        #Colisão entre projétil e personagem
        if(colisaoComPersonagem(pM1, pP)):
            break
        if(colisaoComPersonagem(pM2, pP)):
            break        

        if(posY>0):
            stdscr.addstr(posY, posX, '0')

        event = stdscr.getch()
        if (event == KEY_RIGHT):
            tempo+=1
        if (event == KEY_LEFT):
            tempo-=1
        if (event == KEY_DOWN):
            live = True
            stdscr.notimeout(False)
            stdscr.timeout(100)
        if event == 27:
            break
            
 
telaCheia()      
wrapper(main)