#!/usr/bin/python3

# Generation salles
import random
import math

class Dot:
    def __init__(self, a, b):
        self.x = a
        self.y = b

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    """Renvoie true si le point se trouve dans le rectangle"""
    def is_in(self, rectangle):
        return rectangle.x_min <= self.x <= rectangle.x_max and rectangle.y_min <= self.y <= rectangle.y_max

class Rectangle:
    """On fournit 4 Dot qui vont representer les coins de nos salles et nos couloirs (on parcours les coins dans l'ordre horaire en commencant par le coins en haut à gauche)"""
    def __init__(self, a, b, c, d):
        self.corners = [a, b, c, d]
        self.x_max = b.x
        self.x_min = a.x
        self.y_max = a.y
        self.y_min = d.y

    """Renvoie true s'il y a une collision entre deux salles"""
    def intersection(self, room):
        return self.corners[0].is_in(room) or self.corners[1].is_in(room) or self.corners[2].is_in(room) or self.corners[3].is_in(room) or room.corners[0].is_in(self) or room.corners[1].is_in(self) or room.corners[2].is_in(self) or room.corners[3].is_in(self) or (room.x_min <= self.x_min <= self.x_max <= room.x_max and self.y_min <= room.y_min <= room.y_max <= self.y_max) or (room.y_min <= self.y_min <= self.y_max <= room.y_max and self.x_min <= room.x_min <= room.x_max <= self.x_max) or (self.x_min <= room.x_min <= room.x_max <= self.x_max and room.y_min <= self.y_min <= self.y_max <= room.y_max) or (self.y_min <= room.y_min <= room.y_max <= self.y_max and room.x_min <= self.x_min <= self.x_max <= room.x_max)

    """Renvoit un Dot qui represente le centre d'un rectangle """
    def center(self):
        return Dot((self.x_max - self.x_min)/2 + self.x_min, (self.y_max - self.y_min)/2 + self.y_min)

    """Calcule la distance euclidienne entre 2 rectangles"""
    def distance(self, r):
        return math.sqrt((self.center().x - r.center().x)**2 + (self.center().y - r.center().y)**2)

    """Prend en argument la liste des salles et trouve dans cette liste la salle la plus proche de self"""
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

    def __str__(self):
        return str(self.corners[0]) + ", " + str(self.corners[1]) + ", " + str(self.corners[2]) + ", " + str(self.corners[3])

"""Genère une salle dans un plan de dimensions x*y"""
def room_gen(x, y):
    area, h_max, h_min, l_max, l_min = 0, 0, 0, 0, 0
    while not(x * y / 30 <= area <= x * y / 25 and h_min != h_max and l_min != l_max):
        h_max = random.randint(0, y)
        h_min = random.randint(0, h_max)
        l_max = random.randint(0, x)
        l_min = random.randint(0, l_max)
        area = (h_max - h_min) * (l_max - l_min)
    return Rectangle(Dot(l_min, h_max), Dot(l_max, h_max), Dot(l_max, h_min), Dot(l_min, h_min))

"""Genère n salles dans un plan de dimensions x*y"""
def room_disposition(n, x, y):
    res = []
    chambers_generated = 0
    while chambers_generated <= n - 1:
        s = room_gen(x, y)
        Appropriate = True
        for chamber in res:
            if s.intersection(chamber) or 0 <= chamber.x_min - s.x_max < 2 or 0 <= s.x_min - chamber.x_max < 2 or 0 <= s.y_min - chamber.y_max < 2  or 0 <= chamber.y_min - s.y_max < 2:
                Appropriate = False
        if  4 > (s.x_max - s.x_min) or (s.x_max - s.x_min) > 2 * (s.y_max - s.y_min) or 4 > (s.y_max - s.y_min) or (s.y_max - s.y_min) > 2 * (s.x_max - s.x_min):
            Appropriate = False
        if Appropriate:
            res.append(s)
            chambers_generated += 1
    return res

"""Genère un couloir entre deux salles passées en paramètres"""
def corridor_gen(r1, r2):
    res = []
    start = Dot(random.randint(r1.x_min, r1.x_max), random.randint(r1.y_min + 1, r1.y_max))
    end = Dot(random.randint(r2.x_min + 1, r2.x_max), random.randint(r2.y_min + 1, r2.y_max))
    if end.x > start.x:
        res.append(Rectangle(Dot(start.x, start.y), Dot(end.x, start.y), Dot(end.x, start.y), Dot(start.x, start.y)))
    else:
        res.append(Rectangle(Dot(end.x, start.y), Dot(start.x, start.y), Dot(start.x, start.y), Dot(end.x, start.y)))
    if end.y > start.y:
        res.append(Rectangle(Dot(end.x, end.y), Dot(end.x, end.y), Dot(end.x, start.y), Dot(end.x, start.y)))
    else:
        res.append(Rectangle(Dot(end.x, start.y), Dot(end.x, start.y), Dot(end.x, end.y), Dot(end.x, end.y)))
    return res

"""Genère les couloirs réliants toutes les salles du level"""
def level_link(rooms):
    res = []
    to_link = rooms.copy()
    decal = 0
    next = random.choice(to_link)
    to_link.remove(next)
    for i in range(len(to_link)):
        room_to_link = next.find_closest(to_link)
        res += corridor_gen(next, room_to_link[0])
        next = room_to_link[0]
        to_link.remove(next)
        decal += 1
    return rooms + res

"""Affiche toute la disposition des salles et des couloirs générés dans un plan x*y (affichage grossier pour vérifier si tout fonctionne)"""
def representation(rectangles, x, y):
    for j in range(y + 1):
        ligne = str()
        for i in range(x + 1):
            compteur = 0
            for r in rectangles:
                if Dot(i, j).is_in(r):
                    ligne += " "
                    compteur +=1
                    break
            if compteur == 0:
                ligne += "#"
        print(ligne)


a = room_disposition(10, 50, 50)
b = level_link(a)

representation(b, 50, 50)
