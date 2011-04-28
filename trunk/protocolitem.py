import pygame, math, sys, string, os, menu, map, button

class ProtocolItem(button.Button):
    def __init__(self, item):
        font1 = pygame.font.Font(None,24)
        text = font1.render(item.get_name(), 1, (0,0,0))
        super(ProtocolItem, self).__init__(250,250,text,button.OnClick(), "Blank")
        
        self.item = item
        self.linkItems = {}
        i = 0
        num = self.item.get_num_arguments()
        print "Boom"
        print num
        print self.item.get_link_names()
        for name in self.item.get_link_names():
            i += 1
            pos = (i * (self.width/float(num+1)), 0)
            print name, " - ", i, ": ", pos[0]
            orientation = "top"
            if name == "get":
                pos = (0, self.height / 2.0)
                orientation = "left"
                i -= 1
            if name == "next":
                pos = (self.width, self.height - 10)
                orientation = "right"
                i -= 1
            if name == "then":
                pos = (self.width, self.height / 2.0)
                orientation = "right"
                i -= 1
                
            self.linkItems[name] = LinkItem(name, pos, LinkOnClick(name), orientation)
        
    def update(self):
        if self.clickObj.is_clicked():
            x, y = pygame.mouse.get_rel()
            self.pos[0] += x
            self.pos[1] += y
            
    def draw(self, screen):
        if self.nowFocused:
            imageCopy = self.imageFocused.copy()
        else:
            imageCopy = self.image.copy()
        for link in self.linkItems.values():
            link.draw(imageCopy)
        screen.blit(imageCopy, (self.pos[0], self.pos[1]))
        textpos = self.buttonText.get_rect(centerx = screen.get_width()/2)
        screen.blit(self.buttonText,(self.pos[0], self.pos[1]))
        
    def set_link(self, name, buttonB):
        if buttonB == None:
            return self.item.set_link_value(name, None)
        return self.item.set_link_value(name, buttonB.item)
        
    def get_link_position(self, name):
        x,y = self.linkItems[name].get_pos()
        x += self.pos[0]
        y += self.pos[1]
        return (x,y)
        
    def clicked(self, m):
        if not self.enabled:
            return
        x,y = pygame.mouse.get_pos()
        x -= self.pos[0]
        y -= self.pos[1]
        for link in self.linkItems.values():
            if link.check_collision((x,y)):
                link.clicked(m)
                return
        self.clickObj.clicked(m)
        
    def unclicked(self, m):
        if not self.enabled:
            return
        x,y = pygame.mouse.get_pos()
        x -= self.pos[0]
        y -= self.pos[1]
        for link in self.linkItems.values():
            if link.check_collision((x,y)):
                link.unclicked(m)
                return
        self.clickObj.unclicked(m)
        
    def force_unclicked(self):
        for link in self.linkItems.values():
            link.force_unclicked()
        self.clickObj.force_unclicked()
        
class LinkItem(object):
    def __init__(self, name, pos, clickObj, orientation):
        self.width = 10
        self.height = 10
        self.clickObj = clickObj
    
        font1 = pygame.font.Font(None,12)
        text = font1.render(name, 1, (0,0,0))
        
        self.image = pygame.Surface((self.width + text.get_rect().width + 5,self.height), pygame.SRCALPHA, 32).convert_alpha()
        pygame.draw.rect(self.image, (0,0,0), (0,0,self.width,self.height))
        self.rect = self.image.get_rect()
        self.collideRect = self.image.get_rect()
        self.collideRect.width = self.width
        
        if orientation == "top":
            self.image.blit(text, (self.width+5,0))
            self.image = pygame.transform.rotate(self.image,270)
            self.collideRect.midtop = pos
            self.rect.midtop = pos
        if orientation == "left":
            self.image.blit(text, (self.width+5,0))
            self.collideRect.midleft = pos
            self.rect.midleft = pos
        if orientation == "right":
            self.image = pygame.transform.rotate(self.image,180)
            self.image.blit(text, (0,0))
            self.collideRect.midright = pos
            self.rect.midright = pos
        if orientation == "bottom":
            self.image.blit(text, (0,0))
            self.image = pygame.transform.rotate(self.image,90)
            self.collideRect.midbottom = pos
            self.rect.midbottom = pos
            
    def draw(self, screen):
        screen.blit(self.image,self.rect)
        
    def check_collision(self, pos):
        return self.collideRect.collidepoint(pos)
        
    def get_pos(self):
        return self.collideRect.center
        
    def clicked(self, m):
        self.clickObj.clicked(m)
        
    def unclicked(self, m):
        self.clickObj.unclicked(m)
        
    def force_unclicked(self):
        self.clickObj.force_unclicked()
            
            
class LinkOnClick(button.OnClick):
    def __init__(self, name):
        super(LinkOnClick, self).__init__()
        self.name = name
        
    def clicked(self, m):
        super(LinkOnClick, self).clicked(m)
        m.set_start(self.name)
        
    def unclicked(self, m):
        super(LinkOnClick, self).unclicked(m)
        m.set_end(self.name)