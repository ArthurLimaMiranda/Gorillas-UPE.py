import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle
from random import randint
import time, math, ctypes 
import json
from os import path

def telaCheia():
    kernel32 = ctypes.WinDLL('kernel32')
    user32 = ctypes.WinDLL('user32')
    SW_MAXIMIZE = 3
    hWnd = kernel32.GetConsoleWindow()
    user32.ShowWindow(hWnd, SW_MAXIMIZE)

def enter_is_terminate(x):
    #Possibilita fechar as janelas do curses apertando enter
    if x == 10:
        x = 7
    return x

def score(window, pM1, p1Name, p1Score, pM2, p2Name, p2Score, width, height):
    score = str(p1Score)+" VS "+str(p2Score)
    rectangle(window,height-3,5,height-1,width-4)
    window.addstr(height-2, pM1[1],p1Name,curses.A_BOLD)
    window.addstr(height-2, pM2[1]+3,p2Name,curses.A_BOLD)
    window.addstr(height-2, int(width/2)-5, score,curses.A_STANDOUT)
                                                               
def criaJanela(window, texto1, texto2, startRecX,finalRecX,stringX,finalUnidadeX):
                                                                   #Graus ou Velocidade 
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
        velocidade = criaJanela(window,'Velocidade:','3->20m/s',startRecX,finalRecX,stringX,finalVelocidadeX)
        try:
            int(velocidade)
        except:
            NAN=True

        if((not NAN) and int(velocidade)>=3 and int(velocidade)<=20):
            sair=True

        else:
            sair=False

    return int(angulo), int(velocidade)

def atualizar(sprite, frame, yFinal, xFinal, menu = False):
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_YELLOW)
    if ((frame == 0) or (frame == 2)):
        tamanhoJanela = 49
        yInicial = 5
    else:
        tamanhoJanela = 39
        yInicial = 4
        yFinal+=1

    janela = curses.newwin(yInicial,10, yFinal, xFinal)
    if(menu):
        janela.bkgd(' ', curses.color_pair(1) | curses.A_BOLD)
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
    #Posição inicial dos macacos no predio gerada aleatoriamente 
    #entre os dois primeiros ou dois ultimos
    if(pM == 1):
        if (macaco==1):
            xM = 8
            yM = alturaTela-alturaPredio[0]-7
        else:
            xM=larguraTela-16
            yM = alturaTela-alturaPredio[-1]-7

    else:
        if (macaco==1):
            xM = 25
            yM = alturaTela-alturaPredio[1]-7
        else:
            xM = larguraTela-33
            yM = alturaTela-alturaPredio[-2]-7    

    return yM, xM

def colisaoComPersonagem(posicaoMacaco, posicaoProjetil):
    if((posicaoProjetil[1] >= (posicaoMacaco[1]-1)) and (posicaoProjetil[1] <= (posicaoMacaco[1]+9))):
        if((posicaoProjetil[0] <= posicaoMacaco[0]+5) and (posicaoProjetil[0] >= posicaoMacaco[0])):
            return True         
    else:
        return False   

def lancamentoObliquo(macaco, v0, angulo, pM1, pM2, x): 
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
    return v0x, t, x0, posX, y0

def printaPredio(screen, altura, height,  predio):
    for nPredio in range(10):
        for h in range(altura[nPredio]):
            screen.refresh()
            screen.addstr(height-altura[nPredio]+h-2, 5+(nPredio*17), predio[nPredio][h])
  
def lerRanking():

  if (not path.isfile('ranking.json')):
      return False
  else:          
    with open('ranking.json') as fp:
      dadosDaPartida = json.load(fp)

    listaPlayer1 = []
    listaPontosPlayer1 = []
    listaPlayer2 = []
    listaPontosPlayer2 = []
    listaPlayerFinal = []
    listaPontosFinal = []

    for x in range(len(dadosDaPartida)):
      repetidoP1 = 0
      repetidoP2 = 0
      for i in range(len(listaPlayer1)):
        if(listaPlayer1[i] == dadosDaPartida[x]['NomePlayer1']):
          listaPontosPlayer1[i]+=dadosDaPartida[x]['ScorePlayer1']
          repetidoP1+=1
      for i in range(len(listaPlayer2)):
        if(listaPlayer2[i] == dadosDaPartida[x]['NomePlayer2']):
          listaPontosPlayer2[i]+=dadosDaPartida[x]['ScorePlayer2']  
          repetidoP2+=1
      if(repetidoP1 == 0):
        listaPlayer1.append(dadosDaPartida[x]['NomePlayer1'])
        listaPontosPlayer1.append(dadosDaPartida[x]['ScorePlayer1'])
      if(repetidoP2 == 0):
        listaPlayer2.append(dadosDaPartida[x]['NomePlayer2'])
        listaPontosPlayer2.append(dadosDaPartida[x]['ScorePlayer2'])
    

      listaPlayerFinal = listaPlayer1 + listaPlayer2  
      listaPontosFinal = listaPontosPlayer1 + listaPontosPlayer2  

      for i in range(len(listaPlayerFinal)):
        for j in range(i+1, len(listaPlayerFinal)-1):
          if(listaPlayerFinal[i] == listaPlayerFinal[j]):
            listaPontosFinal[i]+=listaPontosFinal[j]  
            listaPlayerFinal.pop(j)
            listaPontosFinal.pop(j)

      for i in range(len(listaPontosFinal)-1):  
        for j in range(len(listaPontosFinal)-1):  
          if(listaPontosFinal[j]<listaPontosFinal[j+1]):  
            tempPontos = listaPontosFinal[j]  
            listaPontosFinal[j] = listaPontosFinal[j+1]  
            listaPontosFinal[j+1] = tempPontos 
            tempPlayer = listaPlayerFinal[j]  
            listaPlayerFinal[j] = listaPlayerFinal[j+1]  
            listaPlayerFinal[j+1] = tempPlayer


    return listaPlayerFinal, listaPontosFinal

def gerarRanking(p1Name, p2Name, p1Score, p2Score, maxRodadas, desafio):
    dadosDaPartida = []

    if(p1Score>p2Score):
        vencedor = p1Name
    elif(p1Score<p2Score):
        vencedor = p2Name
    else:
        vencedor="Empate"

    data = {
      "NomePlayer1": p1Name,
      "ScorePlayer1": p1Score,
      "NomePlayer2": p2Name,
      "ScorePlayer2": p2Score,
      "Rodadas": maxRodadas,
      "Vencedor": vencedor,
      "Desafios": desafio
    }

    if (not path.isfile('ranking.json')):
      with open('ranking.json', 'w') as json_file:
            dadosDaPartida.append(data)
            json.dump(dadosDaPartida, json_file, indent=4, separators=(',',': '))

    else:
        with open('ranking.json') as fp:
          dadosDaPartida = json.load(fp)

        dadosDaPartida.append(data)
        with open('ranking.json', 'w') as json_file:
            json.dump(dadosDaPartida, json_file, indent=4, separators=(',',': '))