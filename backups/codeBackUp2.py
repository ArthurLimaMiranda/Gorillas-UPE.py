import curses
from curses import wrapper, KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP
from curses.textpad import Textbox, rectangle
from random import randint
import time
import math
import ctypes


macaco1 = "@@@@@@@@@@@%%%%%%%@@%%%%%%%@@%%%%%%%@@@@@@@@@@@@@@"
macaco2 = "@@@@@@@@@@@%%%%%%%@@%%%%%%%@@%%%%%%%@@@@@@@@@@@@@@"

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

def entrada(window):
    
    rectangle(window, 1,1,4,20)
    window.addstr(2,2,'Angulo:')
    e1 = curses.newwin(1,4,2,10)
    window.refresh()
    box = Textbox(e1)
    box.edit(enter_is_terminate)
    angulo = box.gather()
    window.addstr(3,2,'Velocidade:')
    e1 = curses.newwin(1,4,3,14)
    window.refresh()
    box = Textbox(e1)
    box.edit(enter_is_terminate)
    velocidade = box.gather()
    
    return int(angulo), int(velocidade)

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

    k=0
    y=0
    debug=True

    x=0
    gravidade = 0.98

    p = True

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
        
        if(p):
            angulo, v0 = entrada(stdscr)
            v0x = v0*math.cos(math.radians(angulo))
            t = math.tan(math.radians(angulo))
            p = False

        if(live):
            x+=1
        
        if(debug):
            posX = pM1[1]+10 + k
            posY = pM1[0]-1 + y
        else:
            x0 = (pM1[1]+10)
            posX = int(x0 + x)
            dX = (posX-x0)

            y0 = (pM1[0]-1)   
            a = (dX*t) - ((gravidade/2)*((dX/v0x)**2))  
            posY = int(y0 - a)
            
        pP = [posY,posX]

        #Colisao entre projétil e prédio
        for i in range(9):
            if(((pP[1] >= ((i*17))) and (pP[1] <= (i*17)+15)) and (pP[0] >= (height-altura[i]))):
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
            debug = True
            k+=1
        if (event == KEY_LEFT):
            debug = True
            k-=1
        if (event == KEY_DOWN):
            debug = True
            y+=1
        if (event == KEY_UP):
            debug = True
            y-=1
        if event == 27:
            debug = False
            live = True
            stdscr.notimeout(False)
            stdscr.timeout(10)
            
 
telaCheia()      
wrapper(main)