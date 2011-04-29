import pygame

# Collaborators:
#   none
# Responsibilities:
#   holds a value to be used in the protocols

class Variable(object):
    def __init__(self, type = "", value = ""):
        # The variable's stored value
        self.value = value
        # The type of variable it is (e.g., "bool", "integer", "unit", etc.)
        self.type = type
        
        self.name = "Variable"
        if self.type != "":
            self.name = self.type
        
        
    def get_type(self):
        return self.type
        
    def set_value(self, value):
        self.value = value
        
    def get_value(self):
        return self.value

    def get_name(self):
        return self.name
        
    # Returns a list of the names of all of the links that
    # variable has. In the case of variable, just get, but
    # the subclasses like function have more
    def get_link_names(self):
        return ["get"]
        
    def set_link_value(self, name, value):
        return False
        
    def get_num_arguments(self):
        return 0