import pygame
import math

from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, dungeon, x, y):
        self.groups = dungeon.sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.dungeon = dungeon
        self.image = pygame.image.load("./assets/knight/knight_f_idle_anim_f0.png")
        # self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
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


    def update(self):
        self.get_keys()
        self.rect.topleft = (self.x + self.speed_x * self.dungeon.dt, self.y + self.speed_y * self.dungeon.dt)

        if not pygame.sprite.spritecollideany(self, self.dungeon.walls) \
                and 0 <= self.rect.topleft[0] < WIDTH \
                and 0 <= self.rect.topleft[1] < HEIGHT:
            self.x += self.speed_x * self.dungeon.dt
            self.y += self.speed_y * self.dungeon.dt
        else:
            self.rect.topleft = (self.x, self.y)
