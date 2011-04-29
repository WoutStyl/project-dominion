import pygame, math, random, operator, soldier
from vector import *

# Ended up being no different from a regular soldier
# If we had a different texture for them then that would be
# used here
class Robot(soldier.Soldier):
    def __init__(self, x = 0.0, y = 0.0, color = (255,0,0)):
        soldier.Soldier.__init__(self, x, y, color)