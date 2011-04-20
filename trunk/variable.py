import pygame

class Variable:
    types = ["bool", "integer", "string", "unit"]
    def __init__(self, type = "", value = None):
        # The variable's stored value
        self.value = value
        # The type of variable it is (e.g., "bool", "integer", "unit", etc.)
        self.type = type
        
    def is_type(self, type):
        return self.type == type
        
    def set_value(self, value):
        self.value = value
        
    def get_value(self):
        return self.value
