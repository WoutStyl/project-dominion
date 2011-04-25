import pygame, math, sys, string, os, menu, map, button

class ProtocolItem(button.Button):
    def __init__(self, item):
        self.item = item
        font1 = pygame.font.Font(None,24)
        text = font1.render(self.item.get_name(), 1, (0,0,0))
        super(ProtocolItem, self).__init__(250,250,text,button.OnClick(), "Blank")
        
    def update(self):
        if self.clickObj.is_clicked():
            x, y = pygame.mouse.get_rel()
            self.pos[0] += x
            self.pos[1] += y