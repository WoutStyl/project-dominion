import variable

class Function(variable.Variable):

    def __init__(self, funcRef, types, type):
        variable.Variable.__init__(self)
        
        self.next = None
        self.funcRef = funcRef
        self.types = types
        self.arguments = dict.fromkeys(self.types.keys())
        
    def get(self):
        pass
        
    def get_next(self):
        pass
    
    def execute(self, unit):
        pass
        
class MoveTowards(Function):
    types = {"target": "unit"}
    
    def execute(self, unit):
        unit.move_towards(self.arguments["otherUnit"])
        
class MoveDirection(Function):
    types = {"direction": "string"}
        
    def execute(self, unit):
        unit.move_direction(self.arguments["direction"])
        
class Stop(Function):
    def execute(self, unit):
        unit.stop()
        
class FireAt(Function):
    types = {"target": "unit"}
    
    def execute(self, unit):
        unit.fire_at(self.arguments["target"])
        
