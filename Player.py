import pygame

from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, dungeon, x, y):
        self.groups = dungeon.sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.dungeon = dungeon
        self.image = pygame.image.load("./assets/0x72_DungeonTilesetII_v1.3/frames/knight_f_idle_anim_f0.png")
        self.image = pygame.transform.scale(self.image, (16, 28))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def move(self, dx = 0, dy = 0):
        if not self.collide_walls(dx, dy): 
            self.x += dx
            self.y += dy

    def collide_walls(self, dx, dy):
        for wall in self.dungeon.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        
        return False

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
