import pygame, button, math, protocolitem, function, variable, soldier, map, menu

# Collaborators:
#   Button
#   Variable/function
# Responsibilities:
#   holds all of the protocol editor's buttons
#   defines interaction between some of the buttons

class ProtocolEditor(menu.Menu):
    def __init__(self):
        super(ProtocolEditor, self).__init__()
        self.stealInput = True
        self.linkPositions = {}
        self.linkItems = {}
        self.error = ""
        
        self.startIndex = 0
        self.startName = ""
        self.endIndex = 0
        self.endName = ""
        
        
        screen = pygame.display.get_surface()
        self.bar_width = screen.get_width()/6
        
        # The two bars on the side with buttons
        self.createBar = pygame.Surface((self.bar_width, screen.get_height()), pygame.SRCALPHA, 32).convert_alpha()
        self.createBar.fill((100,100,100))
        self.selectBar = pygame.Surface((self.bar_width, screen.get_height()), pygame.SRCALPHA, 32).convert_alpha()
        self.selectBar.fill((200,200,200))
        
        self.createBarRect = self.createBar.get_rect()
        self.createBarRect.topleft = (0,0)
        self.selectBarRect = self.selectBar.get_rect()
        self.selectBarRect.topleft = self.createBarRect.topright
        
        font = pygame.font.Font(None, 36)
        
        # The general use buttons
        self.regularButtons = []
        text = font.render("Save", 1, (0,0,0))
        self.regularButtons.append(button.Button(screen.get_width()-100, screen.get_height()-200, text, SaveProtocolOnClick(), "Blank", True))
        #text = font.render("Load", 1, (0,0,0))
        #self.regularButtons.append(button.Button(screen.get_width()-100, screen.get_height()-200, text, LoadProtocolOnClick(), "Blank"))
        text = font.render("Exit", 1, (0,0,0))
        self.regularButtons.append(button.Button(screen.get_width()-100, screen.get_height()-100, text, ExitProtocolOnClick(), "Blank"))
        text = font.render("Delete", 1, (0,0,0))
        self.regularButtons.append(button.Button(self.bar_width * 2, screen.get_height()-100, text, DeleteItemOnClick(), "Blank"))
        
        # The buttons for selecting a type of protocol item
        self.selectedCreateType = ""
        self.selectedCreateIndex = 0
        self.createButtons = []
        text = font.render("Variable", 1, (0,0,0))
        self.createButtons.append(button.Button(0, 0, text, CreateSelectOnClick("Variable", 0), "Blank"))
        text = font.render("Function", 1, (0,0,0))
        self.createButtons.append(button.Button(0, 75, text, CreateSelectOnClick("Function", 1), "Blank"))
        text = font.render("If", 1, (0,0,0))
        self.createButtons.append(button.Button(0, 150, text, CreateSelectOnClick("If", 2), "Blank"))
        text = font.render("While", 1, (0,0,0))
        self.createButtons.append(button.Button(0, 225, text, CreateSelectOnClick("While", 3), "Blank"))
        text = font.render("Foreach", 1, (0,0,0))
        self.createButtons.append(button.Button(0, 300, text, CreateSelectOnClick("Foreach", 4), "Blank"))
        text = font.render("Create", 1, (0,0,0))
        self.createButtons.append(button.Button(0, screen.get_height() - 100, text, CreateOnClick(), "Blank"))
        
        # Buttons for selecting the protocol type's options
        self.selectedOption = ""
        self.selectedOptionIndex = 0
        self.optionButtons = {}
        self.optionButtons["Variable"] = []
        list = self.optionButtons["Variable"]
        text = font.render("Boolean", 1, (0,0,0))
        list.append(button.Button(self.bar_width, 50, text, OptionSelectOnClick("Boolean", 0), "Blank"))
        text = font.render("Integer", 1, (0,0,0))
        list.append(button.Button(self.bar_width, 100, text, OptionSelectOnClick("Integer", 1), "Blank"))
        text = font.render("String", 1, (0,0,0))
        list.append(button.Button(self.bar_width, 150, text, OptionSelectOnClick("String", 2), "Blank"))
        self.optionButtons["Function"] = []
        list = self.optionButtons["Function"]
        i = 1
        for key in soldier.Soldier.commands.keys():
            text = font.render(key, 1, (0,0,0))
            list.append(button.Button(self.bar_width, i * 50, text, OptionSelectOnClick(key, i-1), "Blank"))
            i += 1
            
        self.selectedItemType = ""
        self.selectedItemIndex = 0
        self.protocolItems = []
        
        # Buttons for changing the values of protocol items
        self.selectedValue = ""
        self.selectedValueLabel = ""
        self.valueButtons = {}
        self.valueButtons["Boolean"] = []
        list = self.valueButtons["Boolean"]
        text = font.render("True", 1, (0,0,0))
        list.append(button.Button(self.bar_width, 50, text, ValueSelectOnClick(True, "True"), "Blank"))
        text = font.render("False", 1, (0,0,0))
        list.append(button.Button(self.bar_width, 100, text, ValueSelectOnClick(False, "False"), "Blank"))
        self.valueButtons["Integer"] = []
        list = self.valueButtons["Integer"]
        text = font.render("/\\", 1, (0,0,0))
        list.append(button.Button(self.bar_width, 50, text, AdjustValueOnClick(1), "Blank"))
        text = font.render("\\/", 1, (0,0,0))
        list.append(button.Button(self.bar_width, 100, text, AdjustValueOnClick(-1), "Blank"))
        self.valueButtons["String"] = []
        list = self.valueButtons["String"]
        text = font.render("\"Up\"", 1, (0,0,0))
        list.append(button.Button(self.bar_width, 50, text, ValueSelectOnClick("Up", "\"Up\""), "Blank"))
        text = font.render("\"Down\"", 1, (0,0,0))
        list.append(button.Button(self.bar_width, 100, text, ValueSelectOnClick("Down", "\"Down\""), "Blank"))
        text = font.render("\"Left\"", 1, (0,0,0))
        list.append(button.Button(self.bar_width, 150, text, ValueSelectOnClick("Left", "\"Left\""), "Blank"))
        text = font.render("\"Right\"", 1, (0,0,0))
        list.append(button.Button(self.bar_width, 200, text, ValueSelectOnClick("Right", "\"Right\""), "Blank"))
        text = font.render("\"UpLeft\"", 1, (0,0,0))
        list.append(button.Button(self.bar_width, 250, text, ValueSelectOnClick("UpLeft", "\"UpLeft\""), "Blank"))
        text = font.render("\"UpRight\"", 1, (0,0,0))
        list.append(button.Button(self.bar_width, 300, text, ValueSelectOnClick("UpRight", "\"UpRight\""), "Blank"))
        text = font.render("\"DownLeft\"", 1, (0,0,0))
        list.append(button.Button(self.bar_width, 350, text, ValueSelectOnClick("DownLeft", "\"DownLeft\""), "Blank"))
        text = font.render("\"DownRight\"", 1, (0,0,0))
        list.append(button.Button(self.bar_width, 400, text, ValueSelectOnClick("DownRight", "\"DownRight\""), "Blank"))
        self.valueButtons["If"] = []
        list = self.valueButtons["If"]
        text = font.render("==", 1, (0,0,0))
        list.append(button.Button(self.bar_width, 50, text, ValueSelectOnClick("==", "=="), "Blank"))
        text = font.render("!=", 1, (0,0,0))
        list.append(button.Button(self.bar_width, 100, text, ValueSelectOnClick("!=", "!="), "Blank"))
        text = font.render("<=", 1, (0,0,0))
        list.append(button.Button(self.bar_width, 150, text, ValueSelectOnClick("<=", "<="), "Blank"))
        text = font.render(">=", 1, (0,0,0))
        list.append(button.Button(self.bar_width, 200, text, ValueSelectOnClick(">=", ">="), "Blank"))
        text = font.render("<", 1, (0,0,0))
        list.append(button.Button(self.bar_width, 250, text, ValueSelectOnClick("<", "<"), "Blank"))
        text = font.render(">", 1, (0,0,0))
        list.append(button.Button(self.bar_width, 300, text, ValueSelectOnClick(">", ">"), "Blank"))
        self.valueButtons["While"] = self.valueButtons["If"]
        
        # Create a master list of all buttons to be checked
        self.buttons = self.regularButtons + self.createButtons + self.protocolItems
        for key in sorted(self.optionButtons.keys()):
            # Hide all option buttons
            for aButton in self.optionButtons[key]:
                aButton.set_visible(False)
            self.buttons += self.optionButtons[key]
        for key in sorted(self.valueButtons.keys()):
            # Hide all value changing buttons
            for aButton in self.valueButtons[key]:
                aButton.set_visible(False)
            self.buttons += self.valueButtons[key]
        
    def update(self):
        # Rebuild the master list
        self.buttons = self.regularButtons + self.createButtons + self.protocolItems
        for key in sorted(self.optionButtons.keys()):
            self.buttons += self.optionButtons[key]
        for key in sorted(self.valueButtons.keys()):
            self.buttons += self.valueButtons[key]
        
        # Update all of the buttons
        for b in self.buttons:
            b.update()
            
        # If we have a protocol type selected then make sure it remains focused
        if self.selectedCreateType != "":
            self.createButtons[self.selectedCreateIndex].focus()
            # If we have a type option selected then make sure that remains focused
            if self.selectedOption != "":
                self.optionButtons[self.selectedCreateType][self.selectedOptionIndex].focus()
        # If we have a protocol item selected then make sure that it remains focused
        if self.selectedItemType != "":
            self.buttons[self.selectedItemIndex].focus()
        
        return super(ProtocolEditor, self).update()
        
    def draw(self, screen):
        screen.blit(self.createBar, self.createBarRect)
        screen.blit(self.selectBar, self.selectBarRect)
        
        super(ProtocolEditor, self).draw(screen)
        
        # Draw all of the buttons
        for b in self.buttons:
            b.draw(screen)
            
        # Draw all of the links between protocol items
        for item in self.linkPositions.values():
            for link in item.values():
                if link != None:
                    pygame.draw.line(screen, (255,255,255), link[0], link[1])
            
        # If we're currently dragging a link between protocols
        # then draw the line to our mouse pointer
        if self.startName != "":
            position1 = self.buttons[self.startIndex].get_link_position(self.startName)
            position2 = pygame.mouse.get_pos()
            pygame.draw.line(screen, (255,255,255), position1, position2)
            
        font = pygame.font.Font(None, 36)
        text = font.render(self.error, 1, (255,0,0))
        rect = text.get_rect()
        rect.center = screen.get_rect().center
        screen.blit(text,rect)
            
    
    def handle_event(self, event):
        if event.type != pygame.MOUSEMOTION:
            self.error = ""
        returnValue = super(ProtocolEditor, self).handle_event(event)
        # If we release the mouse then stop drawing any incompleted links
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.reset_link_drag()
                if not returnValue:
                    self.select_option("", 0)
                    self.select_create_type("", 0)
                    self.select_value("", "")
                    self.select_item("")
        return returnValue
                
    # When we've selected a protocol type
    def select_create_type(self, value, index):
        # Hide all of the previous selection's buttons
        self.select_option("", 0)
        if self.selectedCreateType in self.optionButtons.keys():
            for aButton in self.optionButtons[self.selectedCreateType]:
                aButton.set_visible(False)
                
        # Unfocus the previous selection if it exists
        if self.selectedCreateType != "":
            self.createButtons[self.selectedCreateIndex].unfocus()
        self.selectedCreateType = value
        self.selectedCreateIndex = index
        # Unhide all of this selection's associated option buttons
        if self.selectedCreateType in self.optionButtons.keys():
            for aButton in self.optionButtons[self.selectedCreateType]:
                aButton.set_visible(True)
            
        # Make sure we unselect any selected protocol items
        if self.selectedCreateType != "":
            self.select_value("", "")
            self.select_item("")
        
    # Focus the selected option and update values
    def select_option(self, option, index):
        if self.selectedOption != "":
            self.optionButtons[self.selectedCreateType][self.selectedOptionIndex].unfocus()
        self.selectedOption = option
        self.selectedOptionIndex = index
        
    def select_item(self, type):
        # Hide all previous protocol value buttons
        self.select_value("", "")
        if self.selectedItemType in self.valueButtons.keys():
            for aButton in self.valueButtons[self.selectedItemType]:
                aButton.set_visible(False)
                
        # Unfocus the previous protocol item if it exist
        if self.selectedItemType != "":
            self.buttons[self.selectedItemIndex].unfocus()
            
        self.selectedItemType = type
        self.selectedItemIndex = self.index
        
        # Unhide all associated protocol value buttons
        if self.selectedItemType in self.valueButtons.keys():
            for aButton in self.valueButtons[self.selectedItemType]:
                aButton.set_visible(True)
        
        # Unselect all protocol types and options
        if self.selectedItemType != "":
            self.select_option("",0)
            self.select_create_type("", 0)
        
    # If we've selected a new value, set the protocol item to it
    def select_value(self, value, label):
        self.selectedValue = value
        self.selectedValueLabel = label
        
        if self.selectedValue != "":
            self.buttons[self.selectedItemIndex].set_value(value, label)
        
    # Adjust the current value by some amount
    def adjust_value(self, amount):
        # If there's no current value to adjust then retrieve it
        if self.selectedValue == "":
            self.retrieve_value()
        self.select_value(self.selectedValue + amount, str(self.selectedValue + amount))
        
    def retrieve_value(self):
        if self.selectedItemType != "":
            self.selectedValue = self.buttons[self.selectedItemIndex].get_value()
            self.selectedLabel = str(self.selectedValue)
        
    # Remove the protocol item fom the list and remove all links to it
    def delete_item(self):
        if self.selectedItemType == "":
            return
        self.protocolItems.remove(self.buttons[self.selectedItemIndex])
        # A link is stored going both ways, so remove it from both directions
        if self.selectedItemIndex in self.linkItems.keys():
            for key in self.linkItems[self.selectedItemIndex].keys():
                links = self.linkItems[self.selectedItemIndex]
                if links[key] != None:
                    self.buttons[links[key][0]].set_link(links[key][1], None)
                    self.linkItems[links[key][0]][links[key][1]] = None
                    self.linkPositions[links[key][0]][links[key][1]] = None
                    
            for key in self.linkPositions[self.selectedItemIndex].keys():
                self.linkPositions[self.selectedItemIndex][key] = None
                self.linkItems[self.selectedItemIndex][key] = None
            
        self.select_value("", "")
        self.select_item("")
        
    def save(self):
        self.sanitize()
        
    def load(self):
        pass
        
    def exit(self):
        pass
        
    def create_selected(self):
        # Create the appropriate OnClick class for the selected protocol type
        clickType = ItemSelectOnClick(self.selectedCreateType)
        if self.selectedOption != "":
            clickType = ItemSelectOnClick(self.selectedOption)
        if self.selectedOption == "Integer":
            clickType = ItemValueSelectOnClick(self.selectedOption)
            
        # Create the appropriate protocol for the type selected
        if self.selectedCreateType == "Variable":
            if self.selectedOption == "":
                return
            self.protocolItems.append(protocolitem.ProtocolItem(variable.Variable(self.selectedOption),clickType))
        if self.selectedCreateType == "Function" and self.selectedOption != "":
            if self.selectedOption == "":
                return
            arguments = soldier.Soldier.commands[self.selectedOption]
            self.protocolItems.append(protocolitem.ProtocolItem(function.Function(arguments[0], self.selectedOption, arguments[1], arguments[2]),clickType))
        if self.selectedCreateType == "If":
            self.protocolItems.append(protocolitem.ProtocolItem(function.IfStatement(),clickType))
        if self.selectedCreateType == "While":
            self.protocolItems.append(protocolitem.ProtocolItem(function.WhileLoop(),clickType))
        if self.selectedCreateType == "Foreach":
            self.protocolItems.append(protocolitem.ProtocolItem(function.ForeachLoop(),clickType))
            
        # Update part of the master list
        self.buttons = self.regularButtons + self.createButtons + self.protocolItems
        self.selectedItemIndex = len(self.buttons)-1
        self.selectedItemType = self.selectedOption
        # Simulate clicking a value for the protocol item, so that it has some initial value
        if self.selectedCreateType in self.valueButtons.keys():
            self.valueButtons[self.selectedCreateType][0].set_visible(True)
            self.valueButtons[self.selectedCreateType][0].clicked(self)
            self.valueButtons[self.selectedCreateType][0].unclicked(self)
            self.valueButtons[self.selectedCreateType][0].set_visible(False)
        if self.selectedOption in self.valueButtons.keys():
            self.valueButtons[self.selectedOption][0].set_visible(True)
            self.valueButtons[self.selectedOption][0].clicked(self)
            self.valueButtons[self.selectedOption][0].unclicked(self)
            self.valueButtons[self.selectedOption][0].set_visible(False)
            
        self.select_option("", 0)
        self.select_create_type("", 0)
        
    # Set the starting point of a link, clearing any old one that existed
    def set_start(self, name):
        self.startIndex = self.index
        self.startName = name
        
        # Clear the old one if it exists
        if self.buttons[self.startIndex].set_link(self.startName, None):
            # Create the dictionaries if they don't exist
            if self.startIndex not in self.linkPositions.keys():
                self.linkPositions[self.startIndex] = {}
                self.linkItems[self.startIndex] = {}
            # Clear the old links from our list of links
            if self.startName in self.linkItems[self.startIndex].keys() and \
               self.linkItems[self.startIndex][self.startName] != None:
                index = self.linkItems[self.startIndex][self.startName][0]
                name = self.linkItems[self.startIndex][self.startName][1]
                self.linkPositions[index][name] = None
                self.linkItems[index][name] = None
            self.linkPositions[self.startIndex][self.startName] = None
            self.linkItems[self.startIndex][self.startName] = None
        
    def set_end(self, name):
        self.endIndex = self.index
        self.endName = name
        # If it's a bad link, then don't try to make it
        if self.startName == "" or (self.endName == "" and self.startName == "get") or \
           (self.startName == "get" and self.endName == "get") or \
           (self.startName != "get" and self.endName != "get"):
            self.reset_link_drag()
            return
        
        button1 = self.buttons[self.startIndex]
        button2 = self.buttons[self.endIndex]
            
        # Try to make the link in one direction
        if self.set_link(button1, self.startIndex, self.startName, button2, self.endIndex, self.endName):
            return
        # Try it in the other
        if self.set_link(button2, self.endIndex, self.endName, button1, self.startIndex, self.startName):
            return
        
        # No link was made
        self.reset_link_drag()
        
    def set_link(self, button1, index1, name1, button2, index2, name2):
        # Try to set the link
        if button1.set_link(name1,button2):
            position1 = button1.get_link_position(name1)
            position2 = button2.get_link_position(name2)
            # Store the link in one direction
            if not index1 in self.linkPositions.keys():
                self.linkPositions[index1] = {}
                self.linkItems[index1] = {}
            self.linkPositions[index1][name1] = [position1, position2]
            self.linkItems[index1][name1] = [index2, name2]
            # Store in the second
            if not index2 in self.linkPositions.keys():
                self.linkPositions[index2] = {}
                self.linkItems[index2] = {}
            self.linkPositions[index2][name2] = [position2, position1]
            self.linkItems[index2][name2] = [index1, name1]
            self.reset_link_drag()
            return True
        return False
        
    # Clear the values after releasing a link drag
    def reset_link_drag(self):
        self.startIndex = 0
        self.startName = ""
        self.endIndex = 0
        self.endName = ""
        
    def sanitize(self):
        numlinks = []
        for item in self.linkItems.keys():
            for name in self.linkItems[item].keys():
                pair = self.linkItems[item][name]
                if pair != None and pair[1] == "get":
                    if pair[0] not in numlinks:
                        numlinks.append(pair[0])
                    elif "function" in self.buttons[pair[0]].get_type():
                        self.error = "Multiple links flow towards a single function"
                        return
        if len(numlinks) >= len(self.protocolItems):
            self.error = "No head node to start from"
            return
        if len(numlinks) < len(self.protocolItems)-1:
            self.error = "More than one unlinked node"
            return
            
        offset = len(self.regularButtons) + len(self.createButtons)
        for i in range(len(self.protocolItems)):
            if not i+offset in numlinks:
                self.error = self.buttons[i+offset].is_sanitized()
                if self.error == "":
                    theMap = map.Map.get()
                    theMap.add_new_protocol(self.buttons[i+offset].get_protocol())
                    self.leave_menu()
                return

# Each of the below classes define what happens on button clicks
# associated with the buttons in the protocol editor
        
class SaveProtocolOnClick(button.OnClick):
    def unclicked(self, m):
        self.isClicked = False
        m.save()
        
class LoadProtocolOnClick(button.OnClick):
    def unclicked(self, m):
        self.isClicked = False
        m.load()
        
class ExitProtocolOnClick(button.OnClick):
    def unclicked(self, m):
        self.isClicked = False
        m.leave_menu()
        
class CreateOnClick(button.OnClick):
    def unclicked(self, m):
        self.isClicked = False
        m.create_selected()
        
class CreateSelectOnClick(button.OnClick):
    def __init__(self, type = "", index = 0):
        super(CreateSelectOnClick, self).__init__()
        self.type = type
        self.index = index
        
    def unclicked(self, m):
        self.isClicked = False
        m.select_create_type(self.type, self.index)
        
class OptionSelectOnClick(button.OnClick):
    def __init__(self, option = "", index = 0):
        super(OptionSelectOnClick, self).__init__()
        self.option = option
        self.index = index
        
    def unclicked(self, m):
        self.isClicked = False
        m.select_option(self.option, self.index)
        
class ItemSelectOnClick(button.OnClick):
    def __init__(self, type = ""):
        super(ItemSelectOnClick, self).__init__()
        self.type = type
        
    def clicked(self, m):
        super(ItemSelectOnClick, self).clicked(m)
        self.isClicked = True
        m.select_item(self.type)
        
class ValueSelectOnClick(button.OnClick):
    def __init__(self, value = "", label = ""):
        super(ValueSelectOnClick, self).__init__()
        self.value = value
        self.label = label
        
    def unclicked(self, m):
        self.isClicked = False
        m.select_value(self.value, self.label)
        m.select_value("", "")
        m.select_item("")
        
class ItemValueSelectOnClick(button.OnClick):
    def __init__(self, type = ""):
        super(ItemValueSelectOnClick, self).__init__()
        self.type = type
        
    def clicked(self, m):
        super(ItemValueSelectOnClick, self).clicked(m)
        self.isClicked = True
        m.select_item(self.type)
        m.retrieve_value()
        
class AdjustValueOnClick(button.OnClick):
    def __init__(self, amount = ""):
        super(AdjustValueOnClick, self).__init__()
        self.amount = amount
    
    def unclicked(self, m):
        self.isClicked = False
        m.adjust_value(self.amount)
        
class DeleteItemOnClick(button.OnClick):
    def unclicked(self, m):
        self.isClicked = False
        m.delete_item()



    
