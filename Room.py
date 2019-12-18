# Generation salles
import random
import pygame
from math import sqrt
from pygame.locals import *

from settings import *
from Wall import *
from Floor import *
from Point import Point


class Room:
    # On fournit 4 Point qui vont representer les coins de nos salles et nos couloirs
    # (on parcours les coins dans l'ordre horaire en commencant par le coins en haut à gauche)
    def __init__(self, a, b, c, d):
        self.corners = [a, b, c, d]
        self.walls = []
        self.floors = []
        self.x_max = b.x
        self.x_min = a.x
        self.y_max = a.y
        self.y_min = d.y

    # Renvoie true s'il y a une collision entre deux salles
    def intersection(self, room):
        return self.corners[0].collide(room) or self.corners[1].collide(room) or self.corners[2].collide(
            room) or self.corners[3].collide(room) or room.corners[0].collide(self) or room.corners[1].collide(
                self) or room.corners[2].collide(self) or room.corners[3].collide(self)

    # Renvoie un Point qui represente le centre d'un rectangle
    def center(self):
        return Point((self.x_max - self.x_min) / 2 + self.x_min, (self.y_max - self.y_min) / 2 + self.y_min)

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

    def init_sprites(self, dungeon, map, corridor=False):
        from Map import Map
        cell = map.cell

        for y in range(self.y_min, self.y_max + 1):
            for x in range(self.x_min, self.x_max + 1):
                self.floors.append(Floor(dungeon, x, y))

        if not corridor:
            for x in range(self.x_min, self.x_max + 1):
                if not cell(self.y_min - 1, x):
                    self.walls.append(Wall(dungeon, x, self.y_min - 1, "FRONT"))
                if not cell(self.y_max + 1, x):
                    self.walls.append(Wall(dungeon, x, self.y_max + 1, "BOTTOM"))
                if cell(self.y_max + 1, x + 1) and not cell(self.y_max + 2, x):  # couloir bas droite
                    self.walls.append(Wall(dungeon, x, self.y_max + 1, "CORNER_BOTTOM_RIGHT"))
                if cell(self.y_max + 1, x - 1):  # couloir bas gauche
                    self.walls.append(Wall(dungeon, x, self.y_max + 1, "CORNER_BOTTOM_LEFT"))

            for y in range(self.y_min - 1, self.y_max + 1):
                if not cell(y, self.x_min - 1):
                    self.walls.append(Wall(dungeon, self.x_min - 1, y, "SIDE_LEFT"))
                if not cell(y, self.x_max + 1):
                    self.walls.append(Wall(dungeon, self.x_max + 1, y, "SIDE_RIGHT"))
                if cell(y + 1, self.x_max + 1):  # couloir haut droite à droite
                    self.walls.append(Wall(dungeon, self.x_max + 1, y, "CORNER_TOP_RIGHT"))
                if cell(y + 1, self.x_min - 1):  # couloir bas gauche à gauche
                    self.walls.append(Wall(dungeon, self.x_min - 1, y, "CORNER_TOP_RIGHT"))
                if cell(y - 1, self.x_max + 1):  # couloir haut gauche à droite
                    self.walls.append(Wall(dungeon, self.x_max + 1, y, "CORNER_TOP_LEFT"))
                if cell(y - 1, self.x_min - 1):  # couloir haut gauche à gauche
                    self.walls.append(Wall(dungeon, self.x_min - 1, y, "CORNER_BOTTOM_RIGHT"))

            self.walls.append(Wall(dungeon, self.x_min - 1, self.y_max + 1, "CORNER_LEFT"))
            self.walls.append(Wall(dungeon, self.x_max + 1, self.y_max + 1, "CORNER_RIGHT"))

        if corridor:
            x = self.x_min

            for y in range(self.y_min - 1, self.y_max + 1):
                if not cell(y - 1, x - 1) and not cell(y, x - 1) and not cell(y + 1, x - 1):
                    self.walls.append(Wall(dungeon, x - 1, y, "SIDE_LEFT"))
                if not cell(y - 1, x + 1) and not cell(y, x + 1) and not cell(y + 1, x + 1):
                    self.walls.append(Wall(dungeon, self.x_max + 1, y, "SIDE_RIGHT"))
                elif cell(y + 1, x + 1) and not cell(y, x + 1):
                    self.walls.append(Wall(dungeon, x + 1, y, "FRONT"))
                # elif cell(y + 1, self.x_max + 1):  # couloir haut droite
                #     self.walls.append(Wall(dungeon, self.x_max + 1, y, "CORNER_TOP_RIGHT"))
                # elif cell(y - 1, self.x_max + 1):  # couloir haut gauche
                #     self.walls.append(Wall(dungeon, self.x_max + 1, y, "CORNER_TOP_LEFT"))

            y = self.y_min
            for x in range(self.x_min - 1, self.x_max + 1):
                if not cell(y - 1, x - 1) and not cell(y - 1, x) and not cell(y - 1, x + 1):
                    if cell(y + 1, x + 1) and not cell(y + 1, x):
                        self.walls.append(Wall(dungeon, x, y + 1, "SIDE_LEFT"))
                    self.walls.append(Wall(dungeon, x, y - 1, "FRONT"))
                if not cell(y + 1, x - 1) and not cell(y + 1, x) and not cell(y + 1, x + 1):
                    if cell(y - 1, x + 1) and not cell(y, x):
                        self.walls.append(Wall(dungeon, x, y + 1, "CORNER_LEFT"))
                    else:
                        self.walls.append(Wall(dungeon, x, y + 1, "BOTTOM"))
                # elif cell(self.y_max + 1, x + 1):  # couloir bas droite
                #     self.walls.append(Wall(dungeon, x, self.y_max + 1, "CORNER_BOTTOM_RIGHT"))
                # elif cell(self.y_max + 1, x - 1):  # couloir bas gauche
                #     self.walls.append(Wall(dungeon, x, self.y_max + 1, "CORNER_BOTTOM_LEFT"))

    def __str__(self):
        return "{" + ', '.join(str(corner) for corner in self.corners) + "}"


# Genère une salle dans un plan de dimensions x*y
def room_gen(x, y):
    area, h_max, h_min, l_max, l_min = 0, 0, 0, 0, 0
    while not (x * y / 30 <= area <= x * y / 25 and h_min != h_max and l_min != l_max):
        h_max = random.randint(1, y)
        h_min = random.randint(1, h_max)
        l_max = random.randint(1, x)
        l_min = random.randint(1, l_max)
        area = (h_max - h_min) * (l_max - l_min)
    return Room(Point(l_min, h_max), Point(l_max, h_max), Point(l_max, h_min), Point(l_min, h_min))


# Genère n salles dans un plan de dimensions x*y
def room_generator(n, dx, dy):
    res = []
    rooms_generated = 0
    while rooms_generated <= n - 1:
        s = room_gen(dx, dy)
        Appropriate = True
        for room in res:
            if s.intersection(
                    room
            ) or 0 <= room.x_min - s.x_max <= 1 or 0 <= s.x_min - room.x_max <= 1 or 0 <= s.y_min - room.y_max <= 1 or 0 <= room.y_min - s.y_max <= 1:
                Appropriate = False
        if 4 > (s.x_max - s.x_min) or (s.x_max - s.x_min) > 2 * (s.y_max - s.y_min) or 4 > (s.y_max - s.y_min) or (
                s.y_max - s.y_min) > 2 * (s.x_max - s.x_min):
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
        corridor.append(
            Room(Point(start.x, start.y), Point(end.x, start.y), Point(end.x, start.y), Point(start.x, start.y)))
    else:
        corridor.append(
            Room(Point(end.x, start.y), Point(start.x, start.y), Point(start.x, start.y), Point(end.x, start.y)))
    if end.y > start.y:
        corridor.append(Room(Point(end.x, end.y), Point(end.x, end.y), Point(end.x, start.y), Point(end.x, start.y)))
    else:
        corridor.append(Room(Point(end.x, start.y), Point(end.x, start.y), Point(end.x, end.y), Point(end.x, end.y)))
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


def display_all(rooms, x, y):
    for j in range(y + 1):
        ligne = str()
        for i in range(x + 1):
            compteur = 0
            for r in rooms:
                if Point(i, j).is_in(r):
                    ligne += " "
                    compteur += 1
                    break
            if compteur == 0:
                ligne += "#"
        print(ligne)


# a = room_generator(10, 50, 50)
# b = level_link(a)
# display_all(a + b, 50, 50)
