# Generation salles
import random
import pygame
from pygame.locals import *

from settings import *
from Wall import *


class Point:
    def __init__(self, a, b):
        self.x = a
        self.y = b

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def is_in(self, room):
        return room.x_min <= self.x <= room.x_max and room.y_min <= self.y <= room.y_max


class Room:
    def __init__(self, dx, dy, c):
        if c == True:
            area, h_max, h_min, l_max, l_min = 0, 0, 0, 0, 0
            while not(dx * dy / 30 <= area <= dx * dy / 25 and h_min != h_max and l_min != l_max):
                h_max = random.randint(0, dy)
                h_min = random.randint(0, h_max)
                l_max = random.randint(0, dx)
                l_min = random.randint(0, l_max)
                area = (h_max - h_min) * (l_max - l_min)
            self.corners = [Point(l_min, h_min), Point(l_max, h_min), Point(l_max, h_max), Point(l_min, h_max)]
            self.x_min = l_min
            self.x_max = l_max
            self.y_min = h_min
            self.y_max = h_max
        else:
            self.corners = [Point(dx - 1, dy + 1), Point(dx + 1, dy + 1), Point(dx + 1, dy - 1), Point(dx - 1, dy - 1)]
            self.x_min = dx - 1
            self.x_max = dx + 1
            self.y_min = dy - 1
            self.y_max = dy + 1
        
        self.walls = []

    def init(self, dungeon):
        for x in range(self.x_min + 1, self.x_max):
            self.walls.append(Wall(dungeon, x, self.y_min, "FRONT"))

        for y in range(self.y_min, self.y_max):
            self.walls.append(Wall(dungeon, self.x_min, y, "SIDE_LEFT"))

        for y in range(self.y_min, self.y_max):
            self.walls.append(Wall(dungeon, self.x_max, y, "SIDE_RIGHT"))

        for x in range(self.x_min + 1, self.x_max):
            self.walls.append(Wall(dungeon, x, self.y_max, "BOTTOM"))

        self.walls.append(Wall(dungeon, self.x_min, self.y_max, "CORNER_LEFT"))
        self.walls.append(Wall(dungeon, self.x_max, self.y_max, "CORNER_RIGHT"))


    def __str__(self):
        return '({}, {}, {}, {})'.format(self.corners[0], self.corners[1], self.corners[2], self.corners[3])

    def intersection(self, s2):
        res = False
        if (s2.x_min < self.x_min <= self.x_max < s2.x_max and self.y_min < s2.y_min <= s2.y_max < self.y_max) or (self.x_min < s2.x_min <= s2.x_max < self.x_max and s2.y_min < self.y_min <= self.y_max < s2.y_max):
            res = True
        else:
            for i in range(4):
                if self.corners[i].is_in(s2) or s2.corners[i].is_in(self):
                    res = True
        return res


def room_generator(dungeon, n, dx, dy):
    res = []
    rooms_generated = 0
    while rooms_generated <= n - 1:
        s = Room(dx, dy, True)
        Appropriate = True
        for room in res:
            if s.intersection(room) or 0 <= room.x_min - s.x_max <= 1 or 0 <= s.x_min - room.x_max <= 1 or 0 <= s.y_min - room.y_max <= 1 or 0 <= room.y_min - s.y_max <= 1:
                Appropriate = False
        if 4 > (s.x_max - s.x_min) or (s.x_max - s.x_min) > 2 * (s.y_max - s.y_min) or 4 > (s.y_max - s.y_min) or (s.y_max - s.y_min) > 2 * (s.x_max - s.x_min):
            Appropriate = False
        if Appropriate:
            res.append(s)
            rooms_generated += 1

    for room in res:
        room.init(dungeon)

    return res


def representation(rooms, dx, dy):
    res = []
    for i in range(dy + 1):
        line = []
        for j in range(dx + 1):
            temp = str()
            for s in rooms:
                if Point(j, i).is_in(s):
                    line.append(1)
                    temp += " "
                    break
            if temp == "":
                line.append(0)
        res.append(line)
    return res


def display_all(r):
    for i in range(len(r)):
        res = str()
        for j in range(len(r[i])):
            if r[i][j] == 0:
                res += " "
            elif r[i][j] == 1:
                res += "#"
        print(res)

# Generation Couloirs
