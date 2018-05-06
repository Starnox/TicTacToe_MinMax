#!/usr/bin/python

import random
import sys
import os
import queue
import Game
from queue import Queue
import PerfectBot


# Main game loop

Harta = [[0 for x in range(0, 3 + 1)] for y in range(0 + 3 + 1)]
newGame = Game.Game()
newGame.printMap()
newGame.play()









