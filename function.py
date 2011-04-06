import variable

class Function(variable.Variable):

    def __init__(self, type = "", functionReference = None, types = {}):
        variable.Variable.__init__(self, type)
        
        self.next = None
        self.functionReference = functionReference
        self.types = types
        self.arguments = dict.fromkeys(self.types.keys())
        
    def get_value(self):
        if self.type == "":
            return None
        temp = dict(self.arguments)
        for key in temp.keys():
            temp[key] = temp[key].get_value()
        return self.functionReference(temp)
        
    def get_next(self):
        return self.next
    
    def execute(self, unit):
        print "hewo"
        if self.type != "":
            return None
        tempDict = dict(self.arguments)
        for key in tempDict.keys():
            tempDict[key] = tempDict[key].get_value()
        self.functionReference(unit, tempDict)
        return self.get_next()
            
class IfStatement(Function):
    def __init__(self, type = "=="):
        Function.__init__(self, type)
        
        self.arguments = {"a": None, "b": None}
        self.then = None
        
    def get_value(self):
        pass
        
    def get_next(self):
        a = self.arguments["a"]
        b = self.arguments["b"]
        if self.type == "==" and a.get_value() == b.get_value():
            return self.then
        if self.type == "!=" and a.get_value() != b.get_value():
            return self.then
        if self.type == "<=" and a.get_value() <= b.get_value():
            return self.then
        if self.type == ">=" and a.get_value() >= b.get_value():
            return self.then
        if self.type == "<" and a.get_value() < b.get_value():
            return self.then
        if self.type == ">" and a.get_value() > b.get_value():
            return self.then
        return self.next
        
    def execute(self, unit):
        return self.get_next()
        
class WhileLoop(IfStatement):
    def __init__(self, type = "=="):
        IfStatement.__init__(self, type)
        
class ForeachLoop(Function):
    def __init__(self, type = ""):
        ForeachLoop.__init__(self, type)
        
        self.arguments = {"list": None}
        self.index = 0
        self.then = None
        self.previousItem = None
        
    def get_value(self):
        tempList = self.arguments["list"].get_value()
        return tempList[index]
        
    def get_next(self):
        tempList = self.arguments["list"].get_value()
        if index < len(tempList):
            return self.then
        return self.next
        
    def execute(self, unit):
        tempList = self.arguments["list"].get_value()
        if self.previousItem == None or self.previousItem == tempList[index]:
            self.index += 1
        return self.get_next()
        
# class MoveTowards(Function):
    # types = {"target": "unit"}
    
    # def execute(self, unit):
        # unit.move_towards(self.arguments["otherUnit"])
        
# class MoveDirection(Function):
    # types = {"direction": "string"}
        
    # def execute(self, unit):
        # unit.move_direction(self.arguments["direction"])
        
# class Stop(Function):
    # def execute(self, unit):
        # unit.stop()
        
# class FireAt(Function):
    # types = {"target": "unit"}
    
    # def execute(self, unit):
        # unit.fire_at(self.arguments["target"])
        
