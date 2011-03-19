import pygame, math, random, operator, soldier
from vector import *

class Robot(soldier.Soldier):
    def __init__(self, x = 0.0, y = 0.0):
        soldier.Soldier.__init__(self, x, y)