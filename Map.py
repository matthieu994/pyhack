from ast import literal_eval as make_tuple
import pygame
from settings import *

from Room import *


class Map:
    def __init__(self, dungeon):
        self.dungeon = dungeon

        try:
            self.read()
        except IOError as error:
            self.generate()

    # Read the save file
    def read(self):
        save = open(MAP_SAVE, 'rt')
        next(save)

        self.rooms = []
        for line in save:
            if "corridors" in line or not line:
                break
            room = line[1:-2].split(', ')
            self.rooms.append(
                Room(
                    Point(make_tuple(room[0])[0],
                          make_tuple(room[0])[1]),
                    Point(make_tuple(room[1])[0],
                          make_tuple(room[1])[1]),
                    Point(make_tuple(room[2])[0],
                          make_tuple(room[2])[1]),
                    Point(make_tuple(room[3])[0],
                          make_tuple(room[3])[1]),
                ))

        self.corridors = []
        for line in save:
            corridor = line[1:-2].split(', ')
            self.corridors.append(
                Room(
                    Point(make_tuple(corridor[0])[0],
                          make_tuple(corridor[0])[1]),
                    Point(make_tuple(corridor[1])[0],
                          make_tuple(corridor[1])[1]),
                    Point(make_tuple(corridor[2])[0],
                          make_tuple(corridor[2])[1]),
                    Point(make_tuple(corridor[3])[0],
                          make_tuple(corridor[3])[1]),
                ))

        self.grid = representation(self.rooms + self.corridors, MAP_WIDTH, MAP_HEIGHT)

        for room in self.rooms:
            room.init_sprites(self.dungeon, self)
        for corridor in self.corridors:
            corridor.init_sprites(self.dungeon, self, True)

    # Save Map to file
    def save(self):
        file = open(FILE_SAVE, 'w+')
        save = open(MAP_SAVE, 'w+')

        # Save map with 0 and 1
        for line in self.grid:
            file.write(''.join(str(v) for v in line) + '\n')

        save.write("rooms: \n" + "\n".join(str(room) for room in self.rooms) + "\n")
        save.write("corridors: \n" + "\n".join(str(corridors) for corridors in self.corridors) + "\n")

    def cell(self, y, x):
        return self.grid[y][x]

    # Genereate Map (first launch)
    def generate(self):
        self.rooms = room_generator(ROOMS, MAP_WIDTH - 1, MAP_HEIGHT - 1)
        self.corridors = level_link(self.rooms)
        self.grid = representation(self.rooms + self.corridors, MAP_WIDTH, MAP_HEIGHT)

        for room in self.rooms:
            room.init_sprites(self.dungeon, self)
        for corridor in self.corridors:
            corridor.init_sprites(self.dungeon, self, True)


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
        x = max(-(self.width - SCREEN_WIDTH) - TILESIZE + 6, x)  # right
        y = max(-(self.height - SCREEN_HEIGHT) - TILESIZE + 6, y)  # bottom

        self.camera = pygame.Rect(x, y, self.width, self.height)
