import pygame, math, random, operator, unit, bullet, function, variable
from vector import *

class Soldier(unit.Unit):
    commands = {}
    
    def __init__(self, x = 0.0, y = 0.0):
        unit.Unit.__init__(self, x, y)
        
        self.speed = 45.0
        self.velocity = Vector(0.0,0.0)
        self.facing = Vector(0.0,1.0)
        self.health = 40
        
        self.refire_t = 5.0
        self.last_fire = 5.0
        self.fire_target = None
        self.p_dir = None
        self.fire = False
        
        self.waitTime = 0
        
        self.protocol = None
        
        #Temporary hardcoded protocol
        self.protocol = function.WhileLoop()
        self.protocol.arguments["a"] = variable.Variable("integer", 1)
        self.protocol.arguments["b"] = variable.Variable("integer", 1)
        
        last = self.protocol
        cmd = Soldier.commands["Move Direction"]
        tmp = function.Function(cmd[0],cmd[1],cmd[2])
        tmp.arguments["direction"] = variable.Variable("string", "Right")
        last.then = tmp
        
        last = tmp
        cmd = Soldier.commands["Wait"]
        tmp = function.Function(cmd[0],cmd[1],cmd[2])
        tmp.arguments["seconds"] = variable.Variable("integer", random.randint(100,200)/100.0)
        last.next = tmp
        
        last = tmp
        cmd = Soldier.commands["Stop"]
        tmp = function.Function(cmd[0],cmd[1],cmd[2])
        last.next = tmp
        
        last = tmp
        cmd = Soldier.commands["Wait"]
        tmp = function.Function(cmd[0],cmd[1],cmd[2])
        tmp.arguments["seconds"] = variable.Variable("integer", random.randint(100,200)/100.0)
        last.next = tmp
        
        last = tmp
        cmd = Soldier.commands["Move Direction"]
        tmp = function.Function(cmd[0],cmd[1],cmd[2])
        tmp.arguments["direction"] = variable.Variable("string", "Down")
        last.next = tmp
        
        last = tmp
        cmd = Soldier.commands["Wait"]
        tmp = function.Function(cmd[0],cmd[1],cmd[2])
        tmp.arguments["seconds"] = variable.Variable("integer", random.randint(100,200)/100.0)
        last.next = tmp
        
        last = tmp
        cmd = Soldier.commands["Stop"]
        tmp = function.Function(cmd[0],cmd[1],cmd[2])
        last.next = tmp
        
        last = tmp
        cmd = Soldier.commands["Wait"]
        tmp = function.Function(cmd[0],cmd[1],cmd[2])
        tmp.arguments["seconds"] = variable.Variable("integer", random.randint(100,200)/100.0)
        last.next = tmp
        
        last = tmp
        cmd = Soldier.commands["Move Direction"]
        tmp = function.Function(cmd[0],cmd[1],cmd[2])
        tmp.arguments["direction"] = variable.Variable("string", "Left")
        last.next = tmp
        
        last = tmp
        cmd = Soldier.commands["Wait"]
        tmp = function.Function(cmd[0],cmd[1],cmd[2])
        tmp.arguments["seconds"] = variable.Variable("integer", random.randint(100,200)/100.0)
        last.next = tmp
        
        last = tmp
        cmd = Soldier.commands["Stop"]
        tmp = function.Function(cmd[0],cmd[1],cmd[2])
        last.next = tmp
        
        last = tmp
        cmd = Soldier.commands["Wait"]
        tmp = function.Function(cmd[0],cmd[1],cmd[2])
        tmp.arguments["seconds"] = variable.Variable("integer", random.randint(100,200)/100.0)
        last.next = tmp
        
        last = tmp
        cmd = Soldier.commands["Move Direction"]
        tmp = function.Function(cmd[0],cmd[1],cmd[2])
        tmp.arguments["direction"] = variable.Variable("string", "Up")
        last.next = tmp
        
        last = tmp
        cmd = Soldier.commands["Wait"]
        tmp = function.Function(cmd[0],cmd[1],cmd[2])
        tmp.arguments["seconds"] = variable.Variable("integer", random.randint(100,200)/100.0)
        last.next = tmp
        
        last = tmp
        cmd = Soldier.commands["Stop"]
        tmp = function.Function(cmd[0],cmd[1],cmd[2])
        last.next = tmp
        
        last = tmp
        cmd = Soldier.commands["Wait"]
        tmp = function.Function(cmd[0],cmd[1],cmd[2])
        tmp.arguments["seconds"] = variable.Variable("integer", random.randint(100,200)/100.0)
        last.next = tmp
        
        tmp.next = self.protocol
        
        
        
        
    def update(self, delta_seconds):
        print "update!"
        if self.last_fire >= self.refire_t:
            self.last_fire = 0
        if self.last_fire >0:
            self.last_fire +=delta_seconds
        
        self.pos += self.velocity * self.speed * delta_seconds
        self.rect.center = self.pos.get()
        
        if self.waitTime > 0:
            self.waitTime -= delta_seconds
        else:
            self.waitTime = 0
            
            print self.protocol
            print self.protocol.get_next()
            if self.protocol != None:
                self.protocol = self.protocol.execute(self)
                
        if self.fire == True:
            self.fire = False
            return bullet.Bullet(self.p_dir, self.pos[0], self.pos[1])

        
    def keep_on_screen(self, max_x, max_y):
        if self.rect.top <= 0 and self.velocity[1] < 0:
            self.velocity[1] = 0
        if self.rect.left <= 0 and self.velocity[0] < 0:
            self.velocity[0] = 0
        if self.rect.bottom >= max_y and self.velocity[1] > 0:
            self.velocity[1] = 0
        if self.rect.right >= max_x and self.velocity[0] > 0:
            self.velocity[0] = 0
            
            
#Protocol Commands
    def move_towards(self, args):
        self.velocity = args["target"].pos - self.pos
        self.velocity.normalize()
        self.facing = Vector(self.velocity[0],self.velocity[1])
        
    def move_direction(self, args):
        direction = args["direction"]
        print "Moving in direction ", direction
        if direction == "Left":
            self.velocity = Vector(-1,0)
        elif direction == "Right":
            self.velocity = Vector(1,0)
        elif direction == "Up":
            self.velocity = Vector(0,-1)
        elif direction == "Down":
            self.velocity = Vector(0,1)
        elif direction == "UpLeft":
            self.velocity = Vector(-1,-1)
            self.velocity.normalize()
        elif direction == "UpRight":
            self.velocity = Vector(1,-1)
            self.velocity.normalize()
        elif direction == "DownLeft":
            self.velocity = Vector(-1,1)
            self.velocity.normalize()
        elif direction == "DownRight":
            self.velocity = Vector(1,1)
            self.velocity.normalize()
        self.facing = Vector(self.velocity[0],self.velocity[1])
        
    def stop(self, args):
        print "stopping"
        self.velocity = Vector(0.0,0.0)
        
    def fire_at(self, target, delta_seconds):
        if(self.last_fire ==0):
            self.last_fire += delta_seconds
            self.fire_target = target
            t_pos = self.fire_target.pos
            t_vel = self.fire_target.velocity * self.fire_target.speed
            p_pos = t_pos + t_vel   #projected position of the target
            self.p_dir = p_pos - self.pos
            self.p_dir.normalize()       #direction to the projected position of the target
            self.fire = True
            #self.last_fire = 1
                 
    def wait(self, args):
        print "wait for me"
        self.waitTime = args["seconds"]
            
    def is_within_distance(self, args):
        target = args["target"]
        distance = args["distance"]
        if self.rect.left > target.rect.right:
            x1 = self.rect.left
            x2 = target.rect.right
        elif self.rect.right < target.rect.left:
            x1 = self.rect.right
            x2 = target.rect.left
        else:
            x1 = self.pos[0]
            x2 = self.pos[0]
            
        if self.rect.top > target.rect.bottom:
            y1 = self.rect.top
            y2 = target.rect.bottom
        elif self.rect.bottom < target.rect.top:
            y1 = self.rect.bottom
            y2 = target.rect.top
        else:
            y1 = self.pos[1]
            y2 = self.pos[1]
            
        vec1 = Vector(x1,y1)
        vec2 = Vector(x2,y2)
        vec = vec1 - vec2
        
        return vec.length() <= distance
        
Soldier.commands = {"Move Towards":         ["",
                                             Soldier.move_towards,
                                             {"target": "unit"}],
                    "Move Direction":       ["",
                                             Soldier.move_direction,
                                             {"direction": "string"}],
                    "Stop":                 ["",
                                             Soldier.stop,
                                             {}],
                    "Fire At":              ["",
                                             Soldier.fire_at,
                                             {"target": "unit"}],
                    "Wait":                 ["",
                                             Soldier.wait,
                                             {"seconds": "integer"}],
                    "Is Within Distance":   ["bool",
                                             Soldier.is_within_distance,
                                             {"target": "unit", "distance": "integer"}]
                    }