import levels
import pygame
from random import randrange


class Map:
    def __init__(self, rooms, width, height):
        self.rooms = levels.generateur_salles(rooms, width, height)
        self.rooms_array = self.representation(width, height)
        self.tiles = load_tiles("./assets/dungeon_tileset.png", 16, 16)

    def representation(self, dx, dy):
        res = []
        for i in range(dy + 1):
            ligne = []
            for j in range(dx + 1):
                temp = str()
                for s in self.rooms:
                    if levels.Point(j, i).appartient(s):
                        ligne.append(1)
                        temp += " "
                        break
                if temp == "":
                    ligne.append(0)
            res.append(ligne)
        return res

    def draw(self, background):
        for room in self.rooms:
            room.draw(background)

        # for row in self.rooms_array:
        #     print(row)
        # print()

        # for x, row in enumerate(self.rooms_array):
        #     print(row)
        #     for y, tile_value in enumerate(row):
        #         if tile_value == 1:
        #             random_floor = randrange(6, 10), randrange(0, 3)
        #             background.blit(self.tiles[random_floor[0]][random_floor[1]], (x * 32, y * 32))
        #         if tile_value == 0:
        #             background.blit(self.tiles[8][7], (x * 32, y * 32))

        pygame.display.update()


def load_tiles(filename, width, height):
    image = pygame.image.load(filename).convert()
    image_width, image_height = image.get_size()
    tile_table = []

    for tile_x in range(0, int(image_width / width)):
        line = []

        for tile_y in range(0, int(image_height / height)):
            rect = (tile_x * width, tile_y * height, width, height)
            tile = image.subsurface(rect)
            tile = pygame.transform.scale(tile, (32, 32))
            line.append(tile)

        tile_table.append(line)

    return tile_table
