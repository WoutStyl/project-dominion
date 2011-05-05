import pygame, math, sys, string, os, menu, map, queueitem
#Responsibilities:
#Draws itself
#Responds to Mouse Position

#Collaborators:
#OnClick
#Mouse
#Surface

class Button(object):
    def __init__(self, x,y, text, clickType,targetImage, focused = False, enabled = True, height = 64, width = 256):
        self.height = height
        self.width = width
        self.pos = [x,y]
        self.nowFocused = focused
        self.name = targetImage
        self.clickObj = clickType
        self.enabledClickObj = clickType
        self.buttonText = text
        self.enabled = True
        
        self.image = self.load_image(targetImage + ".png")
        self.imageFocused = self.load_image(targetImage + "Focused.png")
        self.imageDisabled = self.load_image(targetImage + "Disabled.png")
        self.focused = focused
        self.visible = True
        if not enabled:
            self.disable()
        else:
            if focused:
                self.focus()
            else:
                self.unfocus()
                
    def update(self):
        pass
        
    def draw(self,screen):
        if not self.visible:
            return
        if not self.enabled:
            screen.blit(self.imageDisabled, (self.pos[0], self.pos[1]))
        elif self.nowFocused:
            screen.blit(self.imageFocused, (self.pos[0], self.pos[1]))
        else:
            screen.blit(self.image, (self.pos[0], self.pos[1]))
        textpos = self.buttonText.get_rect(centerx = screen.get_width()/2)
        screen.blit(self.buttonText,(self.pos[0], self.pos[1]))
    def changeImage(self, targetImage):
        #self.image, self.rect = self.load_image(targetImage)
        self.name = targetImage
    def unfocus(self):
        self.nowFocused = False
    def focus(self):
        self.nowFocused = True
    def load_image(self, dispName):
        fullname = os.path.join('images', dispName)
        try:
            image = pygame.transform.scale(pygame.image.load(fullname), (self.width, self.height))
        except pygame.error, message:
            print 'Cannot load image:', self.name
            raise SystemExit, message
        return image.convert()
    def is_mouse_focus(self):
        if not self.enabled or not self.visible:
            return False
        mousePos = pygame.mouse.get_pos()
        if mousePos[0] >= self.pos[0] and mousePos[0] <= self.pos[0]+self.width:
            if mousePos[1] >= self.pos[1] and mousePos[1] <= self.pos[1]+self.height:
                self.focus()
                return True
        return False
        
    def is_enabled(self):
        return self.enabled
    def disable(self):
        self.enabled = False
        
    def enable(self):
        self.enabled = True
        if self.focused:
            self.focus()
        else:
            self.unfocus()
        
    def clicked(self, m):
        if not self.enabled or not self.visible:
            return
        self.clickObj.clicked(m)
        
    def unclicked(self, m):
        if not self.enabled or not self.visible:
            return
        self.clickObj.unclicked(m)
        
    def force_unclicked(self):
        self.clickObj.force_unclicked()
        
    def set_enabled(self, value):
        if value is True:
            self.enable()
        else:
            self.disable()
    def set_visible(self, value):
        self.visible = value

#Responsibilities
#Defines logic for click events

#Collaborators
#Menu   

class OnClick(object):
    def __init__(self):
        self.isClicked = False
            
    def is_clicked(self):
        return self.isClicked
        
    def clicked(self, m):
        pygame.mouse.get_rel()
        self.isClicked = True
        
    def unclicked(self, m):
        self.isClicked = False
        
    def force_unclicked(self):
        self.isClicked = False

class StartOnClick(OnClick) :
    def unclicked(self, m):
        super(StartOnClick, self).unclicked(m)
        self.menu = m
        m.bInMenu = False

class LoadOnClick(OnClick) :
    def unclicked(self, m):
        super(LoadOnClick, self).unclicked(m)
        self.menu = m
        tempMap = map.Map.get()
        tempMap.load(self.mission)
        m.bInMenu = False
        
    def setMission(self, mission):
        self.mission = mission
        
class ExitToMainOnClick(OnClick):
    def unclicked(self,m):
        super(ExitToMainOnClick, self).unclicked(m)
        m.nextMenu = menu.MainMenu()
        
class ExitOnClick(OnClick):
    def unclicked(self,m):
        pygame.quit()

class MissionSelectOnClick(OnClick):
    def unclicked(self,m):
        super(MissionSelectOnClick, self).unclicked(m)
        m.nextMenu = menu.MissionSelectMenu(m)

class SavedMissionSelectOnClick(OnClick):
    def unclicked(self,m):
        super(SavedMissionSelectOnClick, self).unclicked(m)
        m.nextMenu = menu.SavedMissionSelectMenu(m)
                
class SavedCampaignSelectOnClick(OnClick):
    def unclicked(self,m):
        super(SavedCampaignSelectOnClick, self).unclicked(m)
        m.nextMenu = menu.SavedCampaignSelectMenu(m)
        
class SaveMissionOnClick(OnClick):
    def unclicked(self,m):
        super(SaveMissionOnClick, self).unclicked(m)
        map.Map.get().save("savedMissions")

class AddToQueueOnClick(OnClick):
    def __init__(self, building = None):
        self.isClicked = False
        self.building = building
    def unclicked(self,m):
        super(AddToQueueOnClick, self).unclicked(m)
        self.building.add_to_queue()

class BackOnClick(OnClick):
    def unclicked(self, m):
        super(BackOnClick, self).unclicked(m)
        m.leave_menu()

class ProtocolDisplayToggleOnClick(OnClick):
    def __init__(self):
        super(ProtocolDisplayToggleOnClick, self).__init__()
        self.menuVisible = False
    def unclicked(self, m):
        super(ProtocolDisplayToggleOnClick, self).unclicked(m)
        if self.menuVisible is False:
            self.menuVisible = True
        else:
            self.menuVisible = False
        m.set_protocols_visible(self.menuVisible)
    def get_visible(self):
        return self.menuVisible
class SelectProtocolOnClick(OnClick):
    def __init__(self, i):
        super(SelectProtocolOnClick, self).__init__()
        self.buttonIndex = i
        
    def unclicked(self, m):
        super(SelectProtocolOnClick, self).unclicked(m)
        m.select_protocol(self.buttonIndex-1)
class SetProtocolOnClick(OnClick):
    def __init__(self):
        super(SetProtocolOnClick,self).__init__()
    def unclicked(self, m):
        super(SetProtocolOnClick, self).unclicked(m)
        m.set_protocol_for_selection()

class EditProtocolOnClick(OnClick):
    def __init__(self):
        super(EditProtocolOnClick,self).__init__()
    def unclicked(self, m):
        super(EditProtocolOnClick, self).unclicked(m)

class DeleteProtocolOnClick(OnClick):
    def __init__(self):
        super(DeleteProtocolOnClick,self).__init__()
    def unclicked(self, m):
        super(DeleteProtocolOnClick, self).unclicked(m)
        m.delete_protocol()

class NewProtocolOnClick(OnClick):
    def __init__(self):
        super(NewProtocolOnClick,self).__init__()
    def unclicked(self, m):
        super(NewProtocolOnClick, self).unclicked(m)
        m.new_protocol(protocoleditor.ProtocolEditor(m))


import protocoleditor
        
        
                
                
	
		
