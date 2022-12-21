#!/usr/bin/env python3

from copy import deepcopy
import sys
import frames
from asciimatics.paths import Path
from asciimatics.renderers import StaticRenderer, ColourImageFile, FigletText
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.effects import Print, Sprite,Background, BannerText


def demo(screen):
    scenes = []
    centre = (screen.width // 2, screen.height // 2)
    images1 = []
    images2 = []

    path = Path()
    path.jump_to(centre[0]-50, centre[1])
    path.move_straight_to(centre[0], centre[1], 4)
    path.wait(100)
    path2 = Path()
    path2.jump_to(centre[0]+100, centre[1])
    path2.move_straight_to(centre[0]+40, centre[1], 4)
    path2.wait(100)

    for image in frames.Macaco_1_Abertura:
        images1.append(image)
    for image in frames.Macaco_2_Abertura:
        images2.append(image)

    textoIntroducao = ("""Este jogo foi feito pelo aluno Arthur Lima
como projeto da disciplina de Introdução a 
Programação, espero que goste :)""")

    #Title
    effects = [
        Background(screen, bg=Screen.COLOUR_MAGENTA),
        BannerText(screen,
                   ColourImageFile(screen, "logo.png", 16, 0, True),
                   (screen.height - 16) // 2,
                   Screen.COLOUR_BLUE)
    ]
    scenes.append(Scene(effects, 150))


    effects = [
        Sprite(screen, 
              renderer_dict = {
                    "default" : StaticRenderer(images=images1) 
                    },
              path = path, clear = True),
    ]

    scenes.append(Scene(effects, 15))
        
    effects = [
        Sprite(screen, 
              renderer_dict = {
                    "default" : StaticRenderer(images=images2) 
                    },
              path = path2, clear = True),
    ]

    scenes.append(Scene(effects, 15))

    effects = [
        Background(screen, bg=Screen.COLOUR_YELLOW),

        Print(screen, FigletText("Bem vindo"), centre[1]-10,
              colour=Screen.COLOUR_MAGENTA, 
              bg=Screen.COLOUR_YELLOW),
        Print(screen,
              StaticRenderer(images=[textoIntroducao]),
              centre[1]+5,
              colour=Screen.COLOUR_MAGENTA, 
              bg=Screen.COLOUR_YELLOW),
        Print(screen,
              StaticRenderer(images=["< Pressione enter para continuar >"]),
              screen.height - 5,
              bg=Screen.COLOUR_YELLOW)
    ]
    scenes.append(Scene(effects, 0))

    screen.play(scenes, stop_on_resize=True, repeat=False)
