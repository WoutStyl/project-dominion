import pygame, math, sys, string, os, Mission_Wrapper, button

class Menu(object):
    def __init__(self, screen):
        self.buttons = []
        self.screen = screen
        self.index = 0
        self.bInMenu = True
        self.mission = ""
        self.nextMenu = self
            
            
    def addButton(self, x,y,text,clicktype, targetImage = "Blank"):
        # print len(self.buttons)
        if len(self.buttons) == 0:
            theButton = button.Button(x,y,text,clicktype,targetImage,True)
                
        else:
            theButton = button.Button(x,y,text,clicktype,targetImage,False)
        self.buttons.append(theButton)
    def draw(self,screen):
        for b in self.buttons:
            b.draw(screen)
    def handle_event(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                print "Keypress Down: "
                self.buttons[self.index].nowFocused = False
                self.index -= 1
                if self.index < 0:
                        self.index = len(self.buttons)-1
                print self.index
                self.buttons[self.index].nowFocused = True
            if event.key == pygame.K_DOWN:
                print "Keypress Up: "
                self.buttons[self.index].nowFocused = False
                self.index += 1
                if self.index >= len(self.buttons):
                        self.index = 0
                print self.index
                self.buttons[self.index].nowFocused = True
            if event.key == pygame.K_RETURN:
                print "Return!"
                self.buttons[self.index].clickObj.isClicked(self)
            if event.key == pygame.K_ESCAPE:
                self.leaveMenu()
        if event.type == pygame.USEREVENT+1:
            print "YAY!"
            self.bInMenu = False
        if event.type == pygame.QUIT:
            sys.exit(0)
    def update(self):
        if(self.bInMenu):
            for event in pygame.event.get():
                self.handle_event(event)
        return self.nextMenu
    def leaveMenu(self):
        self.bInMenu = False
            

            

