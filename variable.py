import pygame

class Variable:
    #types = ["bool", "integer", "string", "unit"]
    def __init__(self, type = "", value = None):
        # The variable's stored value
        self.value = value
        # The type of variable it is (e.g., "bool", "integer", "unit", etc.)
        self.type = type
        
        self.name = "Variable"
        if self.type != "":
            self.name = self.type
        
        
    def is_type(self, type):
        return self.type == type
        
    def set_value(self, value):
        self.value = value
        
    def get_value(self):
        return self.value

    def get_name(self):
        return self.name