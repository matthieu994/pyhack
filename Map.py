import pygame
from settings import *

from Room import *


class Map:
    def __init__(self, dungeon):
        self.dungeon = dungeon

        # try:
            # self.read()
        # except IOError as error:
        self.generate()

    # Read the save file
    def read(self):
        data = []

        file = open(FILE_SAVE, 'rt')

        for line in file:
            data.append(line.strip())

        self.grid = [[0 for x in range(len(data[0]))] for y in range(len(data))]

        for x, rows in enumerate(data):
            for y, value in enumerate(rows):
                self.grid[x][y] = 0 if value == "0" else 1

        print(self.grid)

    # Save Map to file
    def save(self):
        file = open(FILE_SAVE, 'w+')
        
        for line in self.grid:
            file.write(''.join(str(v) for v in line) + '\n')

    # Genereate Map (first launch)
    def generate(self):
        self.rooms = room_generator(self.dungeon, ROOMS, MAP_WIDTH, MAP_HEIGHT)
        self.corridors = level_link(self.rooms)
        self.grid = representation(self.rooms, MAP_WIDTH, MAP_HEIGHT)
        
        for room in self.rooms:
            room.init_sprites(self.dungeon)
        for corridor in self.corridors:
            corridor.init_sprites(self.dungeon)
            

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width, self.height = width, height

    # Return sprite coordinates according to camera current position
    def apply(self, sprite):
        return sprite.rect.move(self.camera.topleft)

    # Move camera with target coordinates
    def update(self, target):
        x = -target.rect.x + int(SCREEN_WIDTH / 2)
        y = -target.rect.y + int(SCREEN_HEIGHT / 2)

        # limit scroll to corners of map real size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - SCREEN_WIDTH), x)  # right
        y = max(-(self.height - SCREEN_HEIGHT), y)  # bottom

        self.camera = pygame.Rect(x, y, self.width, self.height)