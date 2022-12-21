import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle
from asciimatics.screen import Screen
from random import randint
import time, math, ctypes 
import funcoes, frames, abertura, menu


def main(stdscr):
    funcoes.telaCheia
    Screen.wrapper(abertura.demo)
    curses.curs_set(0)
    stdscr.notimeout(True)
    height,width = stdscr.getmaxyx()

    sair = False
    while(not sair):
        p1Name, p2Name, gravidade, maxRodadas, desafio = menu.menu(stdscr)

        """p1Name = "Teste"
        p2Name = "Teste"
        gravidade = 9.8
        maxRodadas = 3
        desafio = '12'"""

        gravidade = float(gravidade)/10
        maxRodadas = int(maxRodadas)
        desafio_01 = desafio_02 = False
        for dn in range(len(desafio)):
            if(desafio[dn] == '1'):
                desafio_01 = True
            if(desafio[dn] == '2'):
                desafio_02 = True

        p1Score = 0
        p2Score = 0
        rodadas = 0
        fim = False
        while (not fim):
            live = False
            newShot = True
            shot = False
            tiros = 0
            tempo = 0
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
                predio[i] = funcoes.criarPredio(altura[i])

            #Geração da posição dos macacos
            pM1 = funcoes.predioMacaco(1,altura, height, width)
            pM2 = funcoes.predioMacaco(2,altura, height, width)

            if(rodadas >= maxRodadas):
                funcoes.gerarRanking(p1Name, p2Name, p1Score, p2Score, maxRodadas, desafio)
                fim = True

            reset = False
            while not reset:
                if(desafio_02 and tiros == 6):
                    reset = True
                else:
                    stdscr.clear()
                    stdscr.refresh()
                    funcoes.printaPredio(stdscr, altura, height, predio)
                    stdscr.refresh()
                    funcoes.score(stdscr, pM1, p1Name, p1Score, pM2, p2Name, p2Score, width, height)

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

                    funcoes.atualizar(frames.macaco_Player1, frameM1, pM1[0], pM1[1])
                    funcoes.atualizar(frames.macaco_Player2, frameM2, pM2[0], pM2[1])
                    
                    if (live == True):
                        stdscr.notimeout(False)
                        stdscr.timeout(95) 
                        if(desafio_01):
                            tempo+=1
                            if(tempo == 140):
                                live = False
                                newShot = True
                                tiros+=1
                                macaco = 1-macaco

                        x+=1
                    if(newShot == True):
                        angulo, v0 = funcoes.entrada(macaco, stdscr, width)
                        tempo = 0
                        x = 0
                        live = True
                        shot = True
                    
                    v0x, t, x0, posX, y0 = funcoes.lancamentoObliquo(macaco, v0, angulo, pM1, pM2, x)

                    dX = (posX-x0)  
                    a = (dX*t) - ((gravidade/2)*((dX/v0x)**2))  
                    posY = int(y0 - a)
                        
                    pP= [posY, posX]
                    newShot = False

                    #Colisao entre projétil e prédio
                    for i in range(10):
                        if(((pP[1] >= (5+(i*17))) and (pP[1] <= (i*17)+20)) and (pP[0] >= (height-2-altura[i]))):
                            intervalo = list(predio[i][height-pP[0]-2-altura[i]])
                            if (intervalo[pP[1]-5-(i*17)] != ' '):
                                intervalo[pP[1]-5-(i*17)] = ' '
                                predio[i][-1-(height-2-pP[0])] = ''.join(intervalo)
                                stdscr.notimeout(True)
                                live = False
                                newShot = True
                                tiros+=1
                                macaco = 1-macaco

                    if((pP[0]>0) and (pP[0]<height) and (pP[1]<width) and (pP[1]>0) and live):
                        stdscr.addstr(pP[0], pP[1], '0')  
                    elif(pP[0]<0 and (pP[1]<width) and (pP[1]>0)):
                        stdscr.addstr(1, pP[1], "^")
                    elif (((pP[1]>width) or (pP[1]<0) or (pP[0]>height)) and live):
                        live = False
                        newShot = True
                        tiros+=1
                        macaco = 1-macaco

                    #Colisão entre projétil e personagem
                    if(funcoes.colisaoComPersonagem(pM1, pP)):
                        reset = True
                        rodadas+=1
                        p2Score+=1
                        macaco = 1
                    if(funcoes.colisaoComPersonagem(pM2, pP)):
                        reset = True
                        rodadas+=1
                        p1Score+=1 
                        macaco = 0   

                    event = stdscr.getch()
                    if event == 27:
                        reset = True
                        fim = True
                        sair = True
                     
funcoes.telaCheia()      
wrapper(main)