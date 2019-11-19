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
