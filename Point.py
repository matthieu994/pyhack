class Point:
    def __init__(self, a, b):
        self.x = a
        self.y = b

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    # Renvoie true si le point se trouve dans le rectangle
    def collide(self, room):
        return room.x_min - 2 <= self.x <= room.x_max + 2 and room.y_min - 2 <= self.y <= room.y_max + 2

    def is_in(self, room):
        return room.x_min <= self.x <= room.x_max and room.y_min <= self.y <= room.y_max
