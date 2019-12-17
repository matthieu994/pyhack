import pygame
from random import randrange

from settings import *

class Wall(pygame.sprite.Sprite):
    def __init__(self, dungeon, x, y, type = "FRONT"):
        self.groups = dungeon.sprites, dungeon.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.dungeon = dungeon
        self.image = self.rand_wall(type)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.x = x
        self.y = y

    # /!\ Reverse coords : x = y
    def rand_wall(self, type):
        if type == "FRONT":
            return self.dungeon.tiles[randrange(1, 5)][0]
        elif type == "SIDE_LEFT":
            return self.dungeon.tiles[0][randrange(0, 4)]
        elif type == "SIDE_RIGHT":
            return self.dungeon.tiles[5][randrange(0, 4)]
        elif type == "BOTTOM":
            return self.dungeon.tiles[randrange(1, 5)][4]
        elif type == "CORNER_LEFT":
            return self.dungeon.tiles[0][4]
        elif type == "CORNER_RIGHT":
            return self.dungeon.tiles[5][4]
        elif type == "CORNER_BOTTOM_LEFT":
            return self.dungeon.tiles[0][5]
        elif type == "CORNER_BOTTOM_RIGHT":
            return self.dungeon.tiles[3][5]
        elif type == "CORNER_TOP_LEFT":
            return self.dungeon.tiles[4][5]
        elif type == "CORNER_TOP_RIGHT":
            return self.rand_wall("FRONT")
