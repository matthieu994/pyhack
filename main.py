import sys
import pygame
from pygame.locals import *

import levels
from Map import *
from settings import *


def init_screen(width, height, title):
    pygame.init()
    pygame.display.set_caption(title)
    pygame.font.init()
    screen = pygame.display.set_mode((width, height))

    return screen


def game_loop(background, salles):

    for salle in salles:
        salle.draw(background)


size = width, height = GRID_WIDTH, GRID_HEIGHT
screen = init_screen(WIDTH, HEIGHT, TITLE)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(BLACK)
screen.blit(background, (0, 0))

dungeon_map = Map(4, width, height)
dungeon_map.draw(background)
levels.display_all(dungeon_map.rooms_array)

# for room in levels.generateur_salles(8, width, height):
# room.draw(background)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == K_q or event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

        screen.blit(background, (0, 0))
        pygame.display.update()
