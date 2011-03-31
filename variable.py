import pygame

class Variable:
    def __init__(self, type = "", value = None):
        self.value = value
        self.type = type
        
    def get(self):
        return self.value