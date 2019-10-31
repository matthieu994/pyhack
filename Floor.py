import pygame
from random import randrange

from settings import *

class Floor(pygame.sprite.Sprite):
    def __init__(self, dungeon, x, y):
        self.groups = dungeon.sprites, dungeon.floors
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.dungeon = dungeon
        self.image = self.dungeon.tiles[randrange(6, 10)][randrange(0, 3)]
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.y = y
        self.x = x
