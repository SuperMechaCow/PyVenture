"""
    PyVenture

    by C. Smith

    A pygame-based project that emulates the classic RPG Maker series
"""
appName = "PyVenture"
appVersion = "001"
appAuthor = "C. Smith"
print(appName + " " + appVersion)
print("by " + appAuthor)

# Import external modules
import pygame

import os

# Import local modules
from lib import config
from lib.game import *

pygame.init()
# Make the Game Display Object
progDisplay = pygame.display.set_mode((config.GU_DISPWIDTH, config.GU_DISPHEIGHT))
# progDisplay = pygame.display.set_mode((config.GU_DISPWIDTH, config.GU_DISPHEIGHT), pygame.FULLSCREEN | pygame.HWSURFACE)
# Set the title bar
pygame.display.set_caption('PyVenture')
# make the clock object
clock = pygame.time.Clock()

pMode = 'titlescreen'
debug = True

if debug:
    pMode = 'game'
    game = Game('maps/proving1')
    game.players.append(Player('draco', 0, 0, 48, 64))
    game.controllers.append(Controller())

while True:
    if pMode == 'game':
        game.gameLoop()

    # Draw the screen
    progDisplay.blit(game.mapWindow, (MU_X, MU_Y))
    progDisplay.blit(game.debugWindow, (UU_DEBUGX, UU_DEBUGY))
    for region in game.redraw:
        pygame.display.update(region)
    # pygame.display.update()
    # Wait until tick (60hz) is over
    clock.tick(60)
