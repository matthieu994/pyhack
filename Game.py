import sys
import pygame
from random import randrange

import Room
from Player import *
from Wall import *
from Floor import *
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
        self.floors = pygame.sprite.Group()
        self.player = Player(self, 0, 0)
        self.rooms = Room.room_generator(self, 4, GRID_WIDTH, GRID_HEIGHT)
        self.rooms_array = Room.representation(self.rooms, GRID_WIDTH, GRID_HEIGHT)

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
        pygame.display.flip()

    def events(self):
        # catch all events here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()

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
