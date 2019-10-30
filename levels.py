#!/usr/bin/python3

# Generation salles
from graph import Graph
import random
import pygame
from pygame.locals import *


class Dot:
    def __init__(self, a, b):
        self.x = a
        self.y = b

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def is_in(self, chamber):
        return chamber.x_min <= self.x <= chamber.x_max and chamber.y_min <= self.y <= chamber.y_max


class Chamber:
    def __init__(self, dx, dy, c):
        if c == True:
            area, h_max, h_min, l_max, l_min = 0, 0, 0, 0, 0
            while not(dx * dy / 30 <= area <= dx * dy / 25 and h_min != h_max and l_min != l_max):
                h_max = random.randint(0, dy)
                h_min = random.randint(0, h_max)
                l_max = random.randint(0, dx)
                l_min = random.randint(0, l_max)
                area = (h_max - h_min) * (l_max - l_min)
            self.corners = [Dot(l_min, h_min), Dot(l_max, h_min), Dot(l_max, h_max), Dot(l_min, h_max)]
            self.x_min = l_min
            self.x_max = l_max
            self.y_min = h_min
            self.y_max = h_max
        else:
            self.corners = [Dot(dx - 1, dy + 1), Dot(dx + 1, dy + 1), Dot(dx + 1, dy - 1), Dot(dx - 1, dy - 1)]
            self.x_min = dx - 1
            self.x_max = dx + 1
            self.y_min = dy - 1
            self.y_max = dy + 1

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

    def draw(self, background):
        from main import WHITE

        rect = Rect(self.corners[0].x, self.corners[0].y, self.x_max - self.x_min, self.y_max - self.y_min)
        pygame.draw.rect(background, WHITE, rect, 0)


def chamber_generator(n, dx, dy):
    res = []
    chambers_generated = 0
    while chambers_generated <= n - 1:
        s = Chamber(dx, dy, True)
        Appropriate = True
        for chamber in res:
            if s.intersection(chamber) or 0 <= chamber.x_min - s.x_max <= 1 or 0 <= s.x_min - chamber.x_max <= 1 or 0 <= s.y_min - chamber.y_max <= 1 or 0 <= chamber.y_min - s.y_max <= 1:
                Appropriate = False
        if  4 > (s.x_max - s.x_min) or (s.x_max - s.x_min) > 2 * (s.y_max - s.y_min) or 4 > (s.y_max - s.y_min) or (s.y_max - s.y_min) > 2 * (s.x_max - s.x_min):
            Appropriate = False
        if Appropriate:
            res.append(s)
            chambers_generated += 1
    return res

def representation(chambers, dx, dy):
    res = []
    for i in range(dy + 1):
        line = []
        for j in range(dx + 1):
            tempo = str()
            for s in chambers:
                if Dot(j, i).is_in(s):
                    line.append(0)
                    tempo += " "
                    break
            if tempo == "":
                line.append(1)
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


a = chamber_generator(6, 40, 40)
b = representation(a, 40, 40)
display_all(b)

# Generation Couloirs
