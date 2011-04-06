import pygame

class Variable:
    def __init__(self, type = "", value = None):
        # The variable's stored value
        self.value = value
        # The type of variable it is (e.g., "bool", "integer", "unit", etc.)
        self.type = type
        
    def get_value(self):
        return self.value