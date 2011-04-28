import pygame, math, random, operator, unit, bullet, function, variable, menu, button
from vector import *

class Soldier(unit.Unit):
    commands = {}
    
    def __init__(self, x = 0, y = 0, color = (255,0,0)):
        unit.Unit.__init__(self, float(x), float(y), color)
        
        self.speed = 45.0
        self.velocity = Vector(0.0,0.0)
        self.facing = Vector(0.0,1.0)
        self.health = 40
        self.waitTime = 0
        
        self.refireT = 5.0
        self.lastFire = 5.0
        self.fireTarget = None
        self.pDir = None
        self.fire = False
        
        self.anim = random.randint(0,200)
        self.animLen = 100;
        self.waitTime = 0
        
        self.protocol = None
        
        #Temporary hardcoded protocol
        self.protocol = function.WhileLoop()
        self.protocol.arguments["a"] = variable.Variable("integer", 1)
        self.protocol.arguments["b"] = variable.Variable("integer", 1)
        
        last = self.protocol
        cmd = Soldier.commands["Move Direction"]
        tmp = function.Function(cmd[0],"Move Direction",cmd[1],cmd[2])
        tmp.arguments["direction"] = variable.Variable("string", "Right")
        last.then = tmp
        
        last = tmp
        cmd = Soldier.commands["Wait"]
        tmp = function.Function(cmd[0],"Wait",cmd[1],cmd[2])
        tmp.arguments["seconds"] = variable.Variable("integer", random.randint(100,200)/100.0)
        last.next = tmp
        
        last = tmp
        cmd = Soldier.commands["Stop"]
        tmp = function.Function(cmd[0],"Stop",cmd[1],cmd[2])
        last.next = tmp
        
        last = tmp
        cmd = Soldier.commands["Wait"]
        tmp = function.Function(cmd[0],"Wait",cmd[1],cmd[2])
        tmp.arguments["seconds"] = variable.Variable("integer", random.randint(100,200)/100.0)
        last.next = tmp
        
        last = tmp
        cmd = Soldier.commands["Move Direction"]
        tmp = function.Function(cmd[0],"Move Direction",cmd[1],cmd[2])
        tmp.arguments["direction"] = variable.Variable("string", "Down")
        last.next = tmp
        
        last = tmp
        cmd = Soldier.commands["Wait"]
        tmp = function.Function(cmd[0],"Wait",cmd[1],cmd[2])
        tmp.arguments["seconds"] = variable.Variable("integer", random.randint(100,200)/100.0)
        last.next = tmp
        
        last = tmp
        cmd = Soldier.commands["Stop"]
        tmp = function.Function(cmd[0],"Stop",cmd[1],cmd[2])
        last.next = tmp
        
        last = tmp
        cmd = Soldier.commands["Wait"]
        tmp = function.Function(cmd[0],"Wait",cmd[1],cmd[2])
        tmp.arguments["seconds"] = variable.Variable("integer", random.randint(100,200)/100.0)
        last.next = tmp
        
        last = tmp
        cmd = Soldier.commands["Move Direction"]
        tmp = function.Function(cmd[0],"Move Direction",cmd[1],cmd[2])
        tmp.arguments["direction"] = variable.Variable("string", "Left")
        last.next = tmp
        
        last = tmp
        cmd = Soldier.commands["Wait"]
        tmp = function.Function(cmd[0],"Wait",cmd[1],cmd[2])
        tmp.arguments["seconds"] = variable.Variable("integer", random.randint(100,200)/100.0)
        last.next = tmp
        
        last = tmp
        cmd = Soldier.commands["Stop"]
        tmp = function.Function(cmd[0],"Stop",cmd[1],cmd[2])
        last.next = tmp
        
        last = tmp
        cmd = Soldier.commands["Wait"]
        tmp = function.Function(cmd[0],"Wait",cmd[1],cmd[2])
        tmp.arguments["seconds"] = variable.Variable("integer", random.randint(100,200)/100.0)
        last.next = tmp
        
        last = tmp
        cmd = Soldier.commands["Move Direction"]
        tmp = function.Function(cmd[0],"Move Direction",cmd[1],cmd[2])
        tmp.arguments["direction"] = variable.Variable("string", "Up")
        last.next = tmp
        
        last = tmp
        cmd = Soldier.commands["Wait"]
        tmp = function.Function(cmd[0],"Wait",cmd[1],cmd[2])
        tmp.arguments["seconds"] = variable.Variable("integer", random.randint(100,200)/100.0)
        last.next = tmp
        
        last = tmp
        cmd = Soldier.commands["Stop"]
        tmp = function.Function(cmd[0],"Stop",cmd[1],cmd[2])
        last.next = tmp
        
        last = tmp
        cmd = Soldier.commands["Wait"]
        tmp = function.Function(cmd[0],"Wait",cmd[1],cmd[2])
        tmp.arguments["seconds"] = variable.Variable("integer", random.randint(100,200)/100.0)
        last.next = tmp
        
        tmp.next = self.protocol
        
        
        
        
    def update(self, deltaSeconds):
        #print "update!"
        if self.lastFire >= self.refireT:
            self.lastFire = 0
        if self.lastFire >0:
            self.lastFire +=deltaSeconds
        
        self.pos += self.velocity * self.speed * deltaSeconds
        self.rect.center = self.pos.get()
        
        if self.waitTime > 0:
            self.waitTime -= deltaSeconds
        else:
            self.waitTime = 0

            if self.protocol !=None:
                    self.protocol = self.protocol.execute(self)
                
        if self.lastFire == 0 and self.fire == True:
            self.lastFire += deltaSeconds
            tPos = self.fireTarget.pos
            tVel = self.fireTarget.velocity * self.fireTarget.speed
            pPos = tPos + tVel   #projected position of the target
            self.pDir = pPos - self.pos
            self.pDir.normalize()       #direction to the projected position of the target
            self.fire = True
            #self.last_fire = 1
            return bullet.Bullet(self.pDir, self.pos[0], self.pos[1])    

        
    def keep_on_screen(self, max_x, max_y):
        if self.rect.top <= 0 and self.velocity[1] < 0:
            self.velocity[1] = 0
        if self.rect.left <= 0 and self.velocity[0] < 0:
            self.velocity[0] = 0
        if self.rect.bottom >= max_y and self.velocity[1] > 0:
            self.velocity[1] = 0
        if self.rect.right >= max_x and self.velocity[0] > 0:
            self.velocity[0] = 0

    def draw(self, screen):
        super(Soldier, self).draw(screen)
        if self.buildMenu is None:
            self.buildMenu = menu.Menu()
            font = pygame.font.Font(None, 36)
            text = font.render("Protocol",1,(0,0,0))
            Click = button.OnClick() #CHANGE to "ChangeProtocolOnClick"
            self.buildMenu.add_button(536,536,text,Click)
        self.buildMenu.update()
        screen.blit(self.image, self.rect)
        if self.isSelected:
            #self.buildMenu.draw(screen)
            self.rect.center = self.pos.get()
            screen.blit(self.image, self.rect)
            
            
#Protocol Commands
    def move_towards(self, arguments):
        self.velocity = arguments["target"].pos - self.pos
        self.velocity.normalize()
        self.facing = Vector(self.velocity[0],self.velocity[1])
        
    def move_direction(self, arguments):
        direction = arguments["direction"]
        #print "Moving in direction ", direction
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
        
    def stop(self, arguments):
        #print "stopping"
        self.velocity = Vector(0.0,0.0)
        
    def fire_at(self, target):
        if target is not None:
            self.fire = True
            self.fireTarget = target
        else:
            self.fire = False
        

    def wait(self, arguments):
        #print "wait for me"
        self.waitTime = arguments["seconds"]
    def is_within_distance(self, arguments):
        target = arguments["target"]
        distance = arguments["distance"]
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
                                             {"target": "Unit"}],
                    "Move Direction":       ["",
                                             Soldier.move_direction,
                                             {"direction": "String"}],
                    "Stop":                 ["",
                                             Soldier.stop,
                                             {}],
                    "Fire At":              ["",
                                             Soldier.fire_at,
                                             {"target": "Unit"}],
                    "Wait":                 ["",
                                             Soldier.wait,
                                             {"seconds": "Integer"}],
                    "Is Within Distance":   ["bool",
                                             Soldier.is_within_distance,
                                             {"target": "unit", "distance": "Integer"}]
                    }
