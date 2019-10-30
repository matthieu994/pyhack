import sys
import pygame
from pygame.locals import *

import levels
from Map import *

WHITE = (240, 240, 240)
BLACK = (20, 20, 20)


def init_screen(width, height, title):
    pygame.init()
    pygame.display.set_caption(title)
    pygame.font.init()
    screen = pygame.display.set_mode((width, height))

    return screen


def game_loop(background, salles):

    for salle in salles:
        salle.draw(background)


size = width, height = 55, 35
screen = init_screen(width * 20, height * 20, "Retro Dungeon")

font = pygame.font.Font(None, 36)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(BLACK)
screen.blit(background, (0, 0))

# dungeon_map = Map(8, width, height)
# dungeon_map.draw(background)

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
