import Room
from Game import *
from settings import *
from Player import *

# for room in Rooms.generateur_salles(8, width, height):
# room.draw(background)

# Main Game object
dungeon = Game()
dungeon.show_start_screen()

while True:
    dungeon.init()
    dungeon.run()
    dungeon.show_go_screen()
