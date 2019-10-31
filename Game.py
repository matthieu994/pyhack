import sys
import pygame
from random import randrange

import Level
from Player import *
from Wall import *
from settings import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(500, 100)
        self.load_data()

    def load_data(self):
        pass

    def init(self):
        self.tiles = load_tiles("./assets/dungeon_tileset.png", 16, 16)
        self.sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.player = Player(self, 0, 0)
        self.rooms = Level.room_generator(self, 4, GRID_WIDTH, GRID_HEIGHT)
        self.rooms_array = Level.representation(self.rooms, GRID_WIDTH, GRID_HEIGHT)

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.sprites.update()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.sprites.draw(self.screen)

        # for x, row in enumerate(self.rooms_array):
        #     # print(row)
        #     for y, tile_value in enumerate(row):
        #         if tile_value == 1:
        #             random_floor = randrange(6, 10), randrange(0, 3)
        #             background.blit(self.tiles[random_floor[0]][random_floor[1]], (y * TILESIZE, x * TILESIZE))
        #         if tile_value == 0:
        #             background.blit(self.tiles[8][7], (y * TILESIZE, x * TILESIZE))

        pygame.display.flip()

    def events(self):
        # catch all events here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    self.quit()
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.player.move(dx=- 1)
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.player.move(dx=1)
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.player.move(dy=- 1)
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.player.move(dy=1)

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass


def load_tiles(filename, width, height):
    image = pygame.image.load(filename).convert()
    image_width, image_height = image.get_size()
    tile_table = []

    for tile_x in range(0, int(image_width / width)):
        line = []

        for tile_y in range(0, int(image_height / height)):
            rect = (tile_x * width, tile_y * height, width, height)
            tile = image.subsurface(rect)
            tile = pygame.transform.scale(tile, (TILESIZE, TILESIZE))
            line.append(tile)

        tile_table.append(line)

    return tile_table
