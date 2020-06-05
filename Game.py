import sys
import pygame
from random import randrange

import Room
from settings import *
from Map import Map, Camera
from Player import *
from Wall import *
from Floor import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        # pygame.key.set_repeat(500, 100)
        self.load_data()

    def load_data(self):
        pass

    def init(self):
        self.tiles = load_tiles("./assets/dungeon_tileset.png", 16, 16)
        self.sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.floors = pygame.sprite.Group()
        self.map = Map(self)
        randRoom = self.map.rooms[randrange(len(self.map.rooms))]
        self.player = Player(self, randRoom.center())
        self.camera = Camera(MAP_WIDTH * TILESIZE, MAP_HEIGHT * TILESIZE)

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        self.map.save()
        pygame.quit()
        sys.exit()

    def update(self):
        self.sprites.update()
        self.player.update()
        self.camera.update(self.player)

    def draw_grid(self):
        for x in range(0, SCREEN_WIDTH, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, y), (SCREEN_WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        # self.draw_grid()
        for sprite in self.sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        
        self.player.draw(self.screen, self.camera)

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


# for room in Rooms.generateur_salles(8, width, height):
# room.draw(background)

# Main Game object
dungeon = Game()
dungeon.show_start_screen()

while True:
    dungeon.init()
    dungeon.run()
    dungeon.show_go_screen()
