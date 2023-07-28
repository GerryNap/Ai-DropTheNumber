import sys
import pygame

from state.Game import Game
from StateManager import StateManager
from state.Home import Home

# INITIAL SETUP
CAPTION = "Drop the number"
WIDTH = 650
HEIGHT = 600
FPS = 35

pygame.init()
pygame.display.set_caption(CAPTION)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

stateManager = StateManager('home')

game = Game(screen, stateManager)
home = Home(screen, stateManager, game)
game.set_home(home)

states = {'home':home,
          'game':game}

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
    states[stateManager.get_state()].run(events)

    pygame.display.update()
    pygame.display.flip()
    clock.tick(FPS)