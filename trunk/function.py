import variable

# Collaborators:
#   self
#   Soldier
# Responsibilities:
#   used to indirectly call functions in soldier

class Function(variable.Variable):
    def __init__(self, type = "", name = "Function", functionReference = None, types = {}):
        super(Function, self).__init__(type)

        # The next function in the protocol chain
        self.next = None
        # The reference to the Soldier member function that this will be calling
        self.functionReference = functionReference
        # A dictionary that relates the argument names to the data type it should be
        self.types = types
        # A dictionary that contains the variables that will be passed to the functionReference when it's called
        self.arguments = dict.fromkeys(self.types.keys())
        self.name = name
        
    # Only functions that are used as variables have a defined
    # type
    def get_type(self):
        if self.type == "":
            return "function"
        return self.type
        
    # Because Functions can be used as Variables we want to be able to retrieve the value
    def get_value(self):
        # Should not attempt to return a value if the Function is not supposed to
        if self.type == "":
            return None
            
        # Retrieve the values before passing them as arguments
        temp = dict(self.arguments)
        for key in temp.keys():
            temp[key] = temp[key].get_value()
            
        return self.functionReference(self, temp)
        
    # Return the next Function in the protocol chain
    def get_next(self):
        return self.next
    
    # Execute the command associated with the Function
    def execute(self, unit):
        # Don't attempt to execute if the function is only meant to be used as a Variable
        if self.type != "":
            return None
            
        # Retrieve the values before passing them as arguments
        tempDict = dict(self.arguments)
        for key in tempDict.keys():
            tempDict[key] = tempDict[key].get_value()
            
        self.functionReference(unit, tempDict)
        return self.get_next()
        
    # This adds the next link and any arguments it takes
    def get_link_names(self):
        if self.type == "":
            return super(Function,self).get_link_names() + self.types.keys() + ["next"]
        return super(Function,self).get_link_names() + self.types.keys()
        
    def set_link_value(self, name, value):
        # Next is a special case and treated differently than just regular arguments
        if name == "next" and (value == None or "function" in value.get_type()):
            self.next = value
            return True
        if name in self.types.keys() and (value == None or self.types[name] in value.get_type()):
            self.arguments[name] = value
            return True
        return False
        
    def get_num_arguments(self):
        return len(self.arguments)
        
    def is_sanitized(self):
        for argument in self.arguments.values():
            if argument == None:
                return "Not all arguments are filled"
            result = argument.is_sanitized()
            if result != "":
                return result
                
        if self.next != None:
            result = self.next.is_sanitized()
            if result != "":
                return result
                
            current = self.next
            while current != None:
                if current.next == self:
                    return "Looped link found"
                current = current.next
        return ""
class IfStatement(Function):
    def __init__(self, type = "=="):
        # Type is used differently for here, it defines what type of comparison is being used
        Function.__init__(self, type)
        
        # IfStatements need and can only have 2 arguments
        self.arguments = {"a": None, "b": None}
        # then defines the Function in the protocol chain that needs to happen if the IfStatement is true
        self.then = None
        self.name = "If"
        
    # Can only be used for its execution, cannot be used as
    # a variable
    def get_type(self):
        return "function"
        
    # IfStatements cannot be used as variables
    def get_value(self):
        pass
        
    # if the statement is true then return the Function referenced by then, otherwise
    # return next
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
        
    # The execution is just deciding whether to go into the if section or not
    def execute(self, unit):
        return self.get_next()
        
    def get_link_names(self):
        return super(IfStatement,self).get_link_names() + ["then"] + self.arguments.keys()
        
    def set_link_value(self, name, value):
        # Next and then are specific cases, and different than
        # regular arguments
        if name == "next" and (value == None or "function" in value.get_type()):
            self.next = value
            return True
        if name == "then" and (value == None or "function" in value.get_type()):
            self.then = value
            return True
        if name in self.arguments.keys():
            if value == None:
                self.arguments[name] = value
                return True
            for str in value.get_type().split():
                if str != "function":
                    self.arguments[name] = value
                    return True
        return False
        
    def is_sanitized(self):
        result = super(IfStatement, self).is_sanitized()
        if result != "":
            return result
            
        if self.then == None:
            return "Empty If block"
        result = self.then.is_sanitized()
        if result != "":
            return result
    
        current = self.then
        if current == self:
            return "Looped link found"
        while current.next != None:
            if current.next == self:
                return "Looped link found"
        current.next = self.next
            
        
# Essentially the same as an IfStatement, the difference will show up in how it's handled
# for the UI, namely that it loops back onto itself
class WhileLoop(IfStatement):
    def __init__(self, type = "=="):
        IfStatement.__init__(self, type)
        self.name = "While"
        
    def is_sanitized(self):
        result = super(WhileLoop, self).is_sanitized()
        if result != "":
            return result
            
        if self.then == None:
            return "Empty While block"
        result = self.then.is_sanitized()
        if result != "":
            return result
    
        current = self.then
        if current == self:
            return "Looped link found"
        while current.next != None:
            if current.next == self:
                return "Looped link found"
        current.next = self
        
# Much different than the WhileLoop and IfStatement as it isn't comparative, it's meant
# to iterate over a list
class ForeachLoop(Function):
    def __init__(self, type = ""):
        Function.__init__(self, type)
        
        self.types = {"list": "list"}
        # Only takes a list as its argument
        self.arguments = {"list": None}
        # Where in the list we are
        self.index = 0
        # Similar to IfStatement it needs to know where to go if we are actually going into the loop
        self.then = None
        # We store the item we used on the last go around
        self.previousItem = None
        self.name = "Foreach"
        
    def get_type(self):
        return "function"
        
    # ForeachLoops can be used as a Variable, so that iterating over the list actually has meaning
    def get_value(self):
        tempList = self.arguments["list"].get_value()
        return tempList[self.index]
        
    # If we haven't finished iterating over the list then return then
    # otherwise return next
    def get_next(self):
        tempList = self.arguments["list"].get_value()
        if self.index < len(tempList):
            return self.then
        self.index = 0
        return self.next
        
    # If we are just starting the loop or the item located at the index from the last go around is still the same
    # then iterate once. This is so that if the list changes between frames, we don't skip items (only one command
    # is executed per frame, so that something like a user-created infinite loop doesn't crash the game). This may
    # need to be expanded to ENSURE that nothing gets skipped though.
    def execute(self, unit):
        tempList = self.arguments["list"].get_value()
        if self.previousItem == None or self.previousItem == tempList[index]:
            self.index += 1
        return self.get_next()
        
    def get_link_names(self):
        return super(ForeachLoop,self).get_link_names() + ["then"]
        
    def set_link_value(self, name, value):
        if name == "next" and (value == None or value.get_type() == "function"):
            self.next = value
            return True
        if name == "then" and (value == None or value.get_type() == "function"):
            self.then = value
            return True
        # Because foreach can be used as a variable (returning
        # the current element in the list) we need to determine
        # what type we'd be considered
        if name == "list":
            if value == None:
                self.arguments[name] = value
                self.type = ""
                return True
            if "list" in value.get_type():
                self.arguments[name] = value
                type = value.get_type()
                if "function" in type:
                    self.type = " ".join(type.split()[2:])
                    return True
                self.type = " ".join(type.split()[1:])
                return True
        return False
        
    def is_sanitized(self):
        result = super(ForeachLoop, self).is_sanitized()
        if result != "":
            return result
            
        if self.then == None:
            return "Empty Foreach block"
        result = self.then.is_sanitized()
        if result != "":
            return result
    
        current = self.then
        if current == self:
            return "Looped link found"
        while current.next != None:
            if current.next == self:
                return "Looped link found"
        current.next = self