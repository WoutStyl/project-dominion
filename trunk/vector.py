class Vector:
    def __init__(self,x=0,y=0):
        self.vec = [x,y]
        
    def get(self):
        return self.vec[:]
        
    def __getitem__(self, key):
        return self.vec[key]
        
    def __setitem__(self, key, value):
        self.vec[key] = value
        
    def scale(self, s):
        return Vector(self[0]*s,self[1]*s)
        
    def __mul__(self, s):
        return Vector(self[0]*s,self[1]*s)
        
    def __div__(self, s):
        return self * (1.0/s)
        
    def __add__(self, b):
        return Vector(self[0]+b[0],self[1]+b[1])
        
    def __sub__(self, b):
        return Vector(self[0]-b[0],self[1]-b[1])
        
    def dot(self, b):
        return self[0]*b[0] + self[1]*b[1]
        
    def length(self):
        return self.dot(self) ** 0.5
        
    def normalize(self):
        l = self.length()
        if l > 0:
            self.vec[0] /= l
            self.vec[1] /= l
