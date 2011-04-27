import pygame, math, sys, string, os, menu, map, button

class ProtocolItem(button.Button):
    def __init__(self, item):
        self.item = item
        font1 = pygame.font.Font(None,24)
        text = font1.render(self.item.get_name(), 1, (0,0,0))
        super(ProtocolItem, self).__init__(250,250,text,LinkOnClick("next"), "Blank")
        
    def update(self):
        if self.clickObj.is_clicked() and pygame.mouse.get_pos()[1] > self.pos[1] and pygame.mouse.get_pos()[1] < self.pos[1] + self.height / 2:
            x, y = pygame.mouse.get_rel()
            self.pos[0] += x
            self.pos[1] += y
        
    def set_link(self, name, buttonB):
        if buttonB == None:
            return self.item.set_link_value(name, None)
        return self.item.set_link_value(name, buttonB.item)
        
    def get_link_position(self, name):
        return self.pos
            
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