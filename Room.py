# Generation salles
import random
import pygame
from math import sqrt
from pygame.locals import *

from settings import *
from Wall import *
from Floor import *


class Point:
    def __init__(self, a, b):
        self.x = a
        self.y = b

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    # Renvoie true si le point se trouve dans le rectangle
    def is_in(self, room):
        return room.x_min <= self.x <= room.x_max and room.y_min <= self.y <= room.y_max


class Room:

    # On fournit 4 Point qui vont representer les coins de nos salles et nos couloirs
    # (on parcours les coins dans l'ordre horaire en commencant par le coins en haut à gauche)
    def __init__(self, a, b, c, d):
        self.corners = [a, b, c, d]
        self.walls = []
        self.floors = []
        self.x_min = a.x
        self.x_max = c.x
        self.y_min = a.y
        self.y_max = c.y

    # Renvoie true s'il y a une collision entre deux salles
    def intersection(self, room):
        return self.corners[0].is_in(room) or self.corners[1].is_in(room) or self.corners[2].is_in(room) or self.corners[3].is_in(room) or room.corners[0].is_in(self) or room.corners[1].is_in(self) or room.corners[2].is_in(self) or room.corners[3].is_in(self) or (room.x_min <= self.x_min <= self.x_max <= room.x_max and self.y_min <= room.y_min <= room.y_max <= self.y_max) or (room.y_min <= self.y_min <= self.y_max <= room.y_max and self.x_min <= room.x_min <= room.x_max <= self.x_max) or (self.x_min <= room.x_min <= room.x_max <= self.x_max and room.y_min <= self.y_min <= self.y_max <= room.y_max) or (self.y_min <= room.y_min <= room.y_max <= self.y_max and room.x_min <= self.x_min <= self.x_max <= room.x_max)

    # Renvoit un Point qui represente le centre d'un rectangle
    def center(self):
        return Point((self.x_max - self.x_min)/2 + self.x_min, (self.y_max - self.y_min)/2 + self.y_min)

    # Calcule la distance euclidienne entre 2 rectangles
    def distance(self, r):
        return sqrt((self.center().x - r.center().x)**2 + (self.center().y - r.center().y)**2)

    # Prend en argument la liste des salles et trouve dans cette liste la salle la plus proche de self
    def find_closest(self, rooms):
        if self != rooms[0]:
            dist = self.distance(rooms[0])
            closest = (rooms[0], 0)
        else:
            dist = self.distance(rooms[1])
            closest = (rooms[1], 0)
        for i in range(len(rooms)):
            if rooms[i] != self:
                d = self.distance(rooms[i])
                if d <= dist:
                    dist = d
                    closest = (rooms[i], i)
        return closest

    def init_sprites(self, dungeon, corridor=False):
        if not corridor:
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

            for y in range(self.y_min + 1, self.y_max):
                for x in range(self.x_min + 1, self.x_max):
                    self.floors.append(Floor(dungeon, x, y))
        else:
            for y in range(self.y_min, self.y_max + 1):
                for x in range(self.x_min, self.x_max + 1):
                    self.floors.append(Floor(dungeon, x, y))

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


# Genère une salle dans un plan de dimensions x*y
def room_gen(x, y):
    area, h_max, h_min, l_max, l_min = 0, 0, 0, 0, 0
    while not(x * y / 30 <= area <= x * y / 25 and h_min != h_max and l_min != l_max):
        h_max = random.randint(0, y)
        h_min = random.randint(0, h_max)
        l_max = random.randint(0, x)
        l_min = random.randint(0, l_max)
        area = (h_max - h_min) * (l_max - l_min)
    return Room(Point(l_min, h_min), Point(l_max, h_min), Point(l_max, h_max), Point(l_min, h_max))


# Genère n salles dans un plan de dimensions x*y
def room_generator(n, dx, dy):
    res = []
    rooms_generated = 0
    while rooms_generated <= n - 1:
        s = room_gen(dx, dy)
        Appropriate = True
        for room in res:
            if s.intersection(room) or 0 <= room.x_min - s.x_max <= 1 or 0 <= s.x_min - room.x_max <= 1 or 0 <= s.y_min - room.y_max <= 1 or 0 <= room.y_min - s.y_max <= 1:
                Appropriate = False
        if 4 > (s.x_max - s.x_min) or (s.x_max - s.x_min) > 2 * (s.y_max - s.y_min) or 4 > (s.y_max - s.y_min) or (s.y_max - s.y_min) > 2 * (s.x_max - s.x_min):
            Appropriate = False
        if Appropriate:
            res.append(s)
            rooms_generated += 1

    return res


# Genère un couloir entre deux salles passées en paramètres
def corridor_gen(r1, r2):
    corridor = []
    start = Point(random.randint(r1.x_min + 1, r1.x_max), random.randint(r1.y_min + 1, r1.y_max))
    end = Point(random.randint(r2.x_min + 1, r2.x_max), random.randint(r2.y_min + 1, r2.y_max))
    if end.x > start.x:
        corridor.append(Room(Point(start.x, start.y - 1), Point(end.x, start.y - 1), Point(end.x, start.y + 1), Point(start.x, start.y + 1)))
    else:
        corridor.append(Room(Point(end.x, start.y - 1), Point(start.x, start.y - 1), Point(start.x, start.y + 1), Point(end.x, start.y + 1)))
    if end.y > start.y:
        corridor.append(Room(Point(end.x - 1, end.y), Point(end.x + 1, end.y), Point(end.x + 1, start.y), Point(end.x - 1, start.y)))
    else:
        corridor.append(Room(Point(end.x - 1, start.y), Point(end.x + 1, start.y), Point(end.x + 1, end.y), Point(end.x - 1, end.y)))
    return corridor


# Genère et retourne les couloirs qui relient les salles du level
def level_link(rooms):
    corridors = []
    to_link = rooms.copy()
    decal = 0
    next_room = random.choice(to_link)
    to_link.remove(next_room)
    for i in range(len(to_link)):
        room_to_link = next_room.find_closest(to_link)
        corridors += corridor_gen(next_room, room_to_link[0])
        next_room = room_to_link[0]
        to_link.remove(next_room)
        decal += 1
    print(i + 1)
    print(len(corridors))
    return corridors


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
