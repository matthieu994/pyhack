import pygame
import math

from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, dungeon, point):
        self.groups = dungeon.sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.dungeon = dungeon
        self.image = pygame.image.load("./assets/knight/knight_f_idle_anim_f0.png")
        self.image = pygame.transform.scale(self.image, (TILESIZE - 5, TILESIZE - 5))
        self.rect = self.image.get_rect()
        self.x = point.x * TILESIZE
        self.y = point.y * TILESIZE
        self.speed_x, self.speed_y = 0, 0

    def get_keys(self):
        self.speed_x, self.speed_y = 0, 0
        keys = pygame.key.get_pressed()

        if KEYBOARD == "US":
            key_up = pygame.K_w
            key_left = pygame.K_a
        else:
            key_up = pygame.K_z
            key_left = pygame.K_q

        if keys[pygame.K_UP] or keys[key_up]:
            self.speed_y = -PLAYER_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.speed_y = PLAYER_SPEED
        if keys[pygame.K_LEFT] or keys[key_left]:
            self.speed_x = -PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.speed_x = PLAYER_SPEED
        if self.speed_x != 0 and self.speed_y != 0:
            self.speed_x *= math.sqrt(2) / 2
            self.speed_y *= math.sqrt(2) / 2\


    def collide_walls(self, coord):
        if coord == 'X':
            collisions = pygame.sprite.spritecollide(self, self.dungeon.walls, False)
            if collisions:
                if self.speed_x > 0:
                    self.x = collisions[0].rect.left - self.rect.width
                if self.speed_x < 0:
                    self.x = collisions[0].rect.right
                self.speed_x = 0
                self.rect.x = self.x
        if coord == 'Y':
            collisions = pygame.sprite.spritecollide(self, self.dungeon.walls, False)
            if collisions:
                if self.speed_y > 0:
                    self.y = collisions[0].rect.top - self.rect.height
                if self.speed_y < 0:
                    self.y = collisions[0].rect.bottom
                self.speed_y = 0
                self.rect.y = self.y

    def update(self):
        self.get_keys()

        if 0 <= self.x + self.speed_x * self.dungeon.dt < MAP_WIDTH * TILESIZE \
                and 0 <= self.y + self.speed_y * self.dungeon.dt < MAP_HEIGHT * TILESIZE:
            self.x += self.speed_x * self.dungeon.dt
            self.y += self.speed_y * self.dungeon.dt
            self.rect.x = self.x
            self.collide_walls('X')
            self.rect.y = self.y
            self.collide_walls('Y')
