import sys
import pygame

from state.Game import Game
from StateManager import StateManager
from state.Home import Home

# INITIAL SETUP
CAPTION = "Drop the number"
WIDTH = 650
HEIGHT = 600
FPS = 45

# 2048 game color library
colors = {0: (204, 192, 179),
          1: (204, 192, 179),
          2: (238, 228, 218),
          4: (237, 224, 200),
          8: (242, 177, 121),
          16: (245, 149, 99),
          32: (246, 124, 95),
          64: (246, 94, 59),
          128: (237, 207, 114),
          256: (237, 204, 97),
          512: (237, 200, 80),
          1024: (237, 197, 63),
          2048: (237, 194, 46),
          'light text': (249, 246, 242),
          'dark text': (119, 110, 101),
          'other': (0, 0, 0),
          'bg': (187, 173, 160)}

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