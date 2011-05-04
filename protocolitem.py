import pygame, math, sys, string, os, menu, map, button

class ProtocolItem(button.Button):
    def __init__(self, item, clickType):
        font1 = pygame.font.Font(None,24)
        text = font1.render(item.get_name(), 1, (0,0,0))
        super(ProtocolItem, self).__init__(250,250,text,clickType, "Blank")
        
        self.item = item
        self.linkItems = {}
        i = 0
        # Create a link tap for each of the arguments that the
        # protocol item takes
        num = self.item.get_num_arguments()
        for name in self.item.get_link_names():
            i += 1
            pos = [i * (self.width/float(num+1)), 0]
            orientation = "top"
            # Orient the tag differently depending on what kind
            if name == "get":
                pos = [0, self.height / 2.0]
                orientation = "left"
                i -= 1
            if name == "next":
                pos = [self.width, self.height - 10]
                orientation = "right"
                i -= 1
            if name == "then":
                pos = [self.width, self.height / 2.0]
                orientation = "right"
                i -= 1
                
            pos[0] += self.pos[0]
            pos[1] += self.pos[1]
            self.linkItems[name] = LinkItem(name, pos, LinkOnClick(name), orientation)
            
            self.label = ""
        
    def update(self):
        # Make the protocol item follow the mouse if it was clicked
        if self.clickObj.is_clicked():
            x, y = pygame.mouse.get_rel()
            self.pos[0] += x
            self.pos[1] += y
            
            # Move the links to coincide with the button movement
            for link in self.linkItems.values():
                link.update(x, y)
            
    def draw(self, screen):
        if self.nowFocused:
            screen.blit(self.imageFocused, (self.pos[0], self.pos[1]))
        else:
            screen.blit(self.image, (self.pos[0], self.pos[1]))
        textpos = self.buttonText.get_rect(centerx = screen.get_width()/2)
        screen.blit(self.buttonText,(self.pos[0], self.pos[1]))
        # Draw the value label if it has one
        if self.label != "":
            font1 = pygame.font.Font(None,18)
            text = font1.render(self.label, 1, (0,0,0))
            rect = text.get_rect()
            rect.center = (self.pos[0] + self.width / 2, self.pos[1] + self.height / 2)
            screen.blit(text,rect)
            
        # Draw all of the links
        for link in self.linkItems.values():
            link.draw(screen)
        
    def set_link(self, name, buttonB):
        if buttonB == None:
            return self.item.set_link_value(name, None)
        return self.item.set_link_value(name, buttonB.item)
        
    def get_link_position(self, name):
        return self.linkItems[name].get_pos()
        
    def set_value(self, value, label):
        self.label = label
        self.item.set_value(value)
        
    # Get the value of the variable
    def get_value(self):
        value = self.item.get_value(None)
        # If it has none, just give it 0
        if value == "":
            value = 0
        self.label = str(value)
        return value
        
    def get_protocol(self):
        return self.item
        
    # When the button's been clicked, first check the link
    # tabs, otherwise use its clickObj
    def clicked(self, m):   
        if not self.enabled:
            return
        pos = pygame.mouse.get_pos()
        for link in self.linkItems.values():
            if link.check_collision(pos):
                link.clicked(m)
                return
        self.clickObj.clicked(m)
        
    # Same as clicked
    def unclicked(self, m):
        if not self.enabled:
            return
        pos = pygame.mouse.get_pos()
        for link in self.linkItems.values():
            if link.check_collision(pos):
                link.unclicked(m)
                return
        self.clickObj.unclicked(m)
        
    # Similar to clicked and unclicked
    def force_unclicked(self):
        for link in self.linkItems.values():
            link.force_unclicked()
        self.clickObj.force_unclicked()
        
    def get_type(self):
        return self.item.get_type()
        
    def is_sanitized(self):
        return self.item.is_sanitized()
        
class LinkItem(object):
    def __init__(self, name, pos, clickObj, orientation):
        self.width = 10
        self.height = 10
        self.clickObj = clickObj
    
        font1 = pygame.font.Font(None,12)
        text = font1.render(name, 1, (0,0,0))
        
        self.image = pygame.Surface((self.width + text.get_rect().width + 5,self.height), pygame.SRCALPHA, 32).convert_alpha()
        pygame.draw.rect(self.image, (0,0,0), (0,0,self.width,self.height))
        self.collideRect = self.image.get_rect()
        self.collideRect.width = self.width
        
        self.pos = pos
        
        # Depending on the orientation, the tab should be
        # displayed differently
        if orientation == "top":
            self.image.blit(text, (self.width+5,0))
            self.image = pygame.transform.rotate(self.image,270)
            self.collideRect.midtop = self.pos
            self.rect = self.image.get_rect()
            self.rect.midtop = self.pos
        if orientation == "left":
            self.image.blit(text, (self.width+5,0))
            self.collideRect.midleft = self.pos
            self.rect = self.image.get_rect()
            self.rect.midleft = self.pos
        if orientation == "right":
            self.image = pygame.transform.rotate(self.image,180)
            self.image.blit(text, (0,0))
            self.collideRect.midright = self.pos
            self.rect = self.image.get_rect()
            self.rect.midright = self.pos
        if orientation == "bottom":
            self.image.blit(text, (0,0))
            self.image = pygame.transform.rotate(self.image,90)
            self.collideRect.midbottom = self.pos
            self.rect = self.image.get_rect()
            self.rect.midbottom = self.pos
            
        self.pos[0] = self.collideRect.centerx
        self.pos[1] = self.collideRect.centery
            
    # Move the tab to follow the button
    def update(self, x, y):
        self.pos[0] += x
        self.pos[1] += y
        self.collideRect.left += x
        self.collideRect.top += y
        self.rect.left += x
        self.rect.top += y
            
    def draw(self, screen):
        screen.blit(self.image,self.rect)
        
    def check_collision(self, pos):
        return self.collideRect.collidepoint(pos)
        
    def get_pos(self):
        return self.pos
        
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
