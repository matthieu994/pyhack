# Generation salles
import random
import sys
import pygame
from pygame.locals import *


class Point:
    def __init__(self, a, b):
        self.x = a
        self.y = b

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def appartient(self, salle):
        return salle.x_min <= self.x <= salle.x_max and salle.y_min <= self.y <= salle.y_max


class Salle:
    def __init__(self, dx, dy):
        surface, h_max, h_min, l_max, l_min = 0, 0, 0, 0, 0
        while not(dx * dy / 30 <= surface <= dx * dy / 25 and h_min != h_max and l_min != l_max):
            h_max = random.randint(0, dy)
            h_min = random.randint(0, h_max)
            l_max = random.randint(0, dx)
            l_min = random.randint(0, l_max)
            surface = (h_max - h_min) * (l_max - l_min)
        self.coins = [Point(l_min, h_min), Point(l_max, h_min), Point(l_max, h_max), Point(l_min, h_max)]
        self.x_min = l_min
        self.x_max = l_max
        self.y_min = h_min
        self.y_max = h_max

    def __str__(self):
        return '({}, {}, {}, {})'.format(self.coins[0], self.coins[1], self.coins[2], self.coins[3])

    def intersection(self, s2):
        res = False
        for i in range(4):
            if self.coins[i].appartient(s2) or s2.coins[i].appartient(self) or (s2.x_min < self.x_min <= self.x_max < s2.x_max and self.y_min < s2.y_min <= s2.y_max < self.y_max) or (self.x_min < s2.x_min <= s2.x_max < self.x_max and s2.y_min < self.y_min <= self.y_max < s2.y_max):
                res = True
        return res

    def draw(self, background):
        from main import WHITE

        rect = Rect(self.coins[0].x, self.coins[0].y, self.x_max - self.x_min, self.y_max - self.y_min)
        pygame.draw.rect(background, WHITE, rect, 0)

        print(self)
        print(rect)


def generateur_salles(n, dx, dy):
    res = []
    salles_generes = 0
    while salles_generes <= n - 1:
        s = Salle(dx, dy)
        convient = True
        for salle in res:
            if s.intersection(salle) or abs(s.x_min - salle.x_max) < 4 or abs(salle.x_min - s.x_max) < 4 or abs(s.y_max - salle.y_min) < 4 or abs(salle.y_max - s.y_min) < 4 or s.x_max - s.x_min < 4 or s.y_max - s.y_min < 4:
                convient = False
        if convient:
            res.append(s)
            salles_generes += 1
            yield s


def affiche_tout(salles, dx, dy):
    for i in range(dy + 1):
        affichage = str()
        for j in range(dx + 1):
            tempo = str()
            for s in salles:
                if Point(j, i).appartient(s) and (j == s.x_min or j == s.x_max) and (i == s.y_min or i == s.y_max):
                    tempo += "."
                    break
                elif Point(j, i).appartient(s) and (j == s.x_min or j == s.x_max):
                    tempo += "|"
                    break
                elif Point(j, i).appartient(s) and (i == s.y_min or i == s.y_max):
                    tempo += "_"
                    break
                elif Point(j, i).appartient(s):
                    tempo += " "
                    break
            if tempo != "":
                affichage += tempo
            else:
                affichage += "#"
        print(affichage)
    return affichage

# ##Generation Couloirs
# class Couloir:
