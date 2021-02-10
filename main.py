import pygame
import numpy as np
import time

pygame.init()

width, height = 500, 500
#Tamaño de la pantalla
screen = pygame.display.set_mode((height, width))

#Color en rgb
bg = 25, 25, 25
screen.fill(bg)

#Celdas del juego
nxC, nyC = 25, 25 #Numero de celdas

dimCW = width / nxC
dimCH = height / nyC

#Estado de las celdas, Vivas = 1, Muertas = 0
gameState = np.zeros((nxC, nyC))

#Automata palo
gameState[5, 3] = 1
gameState[5, 4] = 1
gameState[5, 5] = 1
#Automata movil
gameState[21, 21] = 1
gameState[22, 22] = 1
gameState[22, 23] = 1
gameState[21, 23] = 1
gameState[20, 23] = 1

#Control de pause
pauseExect = False

#Bucle infinito
while True:

    newGameState = np.copy(gameState)

    #Limpiar pantalla
    screen.fill(bg)
    time.sleep(0.2)

    #Eventos por teclado y raton
    ev = pygame.event.get()

    for event in ev:
        if event.type == pygame.KEYDOWN:
            pauseExect = not pauseExect

        mouseClick = pygame.mouse.get_pressed()
        
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            newGameState[celX, celY] = not mouseClick[2]
    
    for y in range(0, nxC):
        for x in range(0, nyC):

            if not pauseExect:
            
                #Calcular el numero de vecinos cercanos
                n_neigh = gameState[(x-1) % nxC, (y-1) % nyC] + \
                        gameState[(x)   % nxC, (y-1) % nyC] + \
                        gameState[(x+1) % nxC, (y-1) % nyC] + \
                        gameState[(x-1) % nxC, (y) % nyC]   + \
                        gameState[(x+1) % nxC, (y) % nyC]   + \
                        gameState[(x-1) % nxC, (y+1) % nyC] + \
                        gameState[(x)   % nxC, (y+1) % nyC] + \
                        gameState[(x+1) % nxC, (y+1) % nyC]

                #Regla 1: Una celula muerta con exactamente 3 vecinas vivas, revive
                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1
                
                #Regla 2: una celula viva con menos de dos o mas de 3 vecinas vivas, muere
                elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x, y] = 0


            #Coordenadas de rectangulos
            poly = [((x)   * dimCW, y     * dimCH),
                    ((x+1) * dimCW, y     * dimCH),
                    ((x+1) * dimCW, (y+1) * dimCH),
                    ((x)   * dimCW, (y+1) * dimCH)]

            #Dibujar celda para cada x, y
            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

    #Actualizar el estado del juego
    gameState = np.copy(newGameState)

    #Actualizar pantalla
    pygame.display.flip()

