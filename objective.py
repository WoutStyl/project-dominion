class Objective:
    #No static variables ...
    def __init__(self,line):
        #the constructor takes the line from the file

        #go through each character
        booltype = True
        boolsubtype = False
        substring = ""
        self.typestring = ""
        self.subtypestring = ""
        self.argstringlist = []
        for char in line:
            #if you are done with the type arg
            if(booltype):
                if(char != ' '):
                    substring = substring + char
                else:
                    booltype = False
                    boolsubtype = True
                    self.typestring = substring
                    substring = ""
                    continue #don't process anymore on this char
                
            #if you are done with the subtype arg
            elif(boolsubtype):
                if(char != ' '):
                    substring = substring + char
                else:
                    boolsubtype = False
                    self.subtypestring = substring
                    substring = ""
                    continue
            #if you are done with both type arg and subtype arg
            elif(not booltype and not boolsubtype):
                if(char != ' '):
                    substring = substring + char
                else:
                    self.argstringlist.append(substring)
                    substring = ""
                    continue
        #End of for loop
        
    #Annnnnnnnnnnd we're done with the constructor
    def save(self):
        stringline = self.typestring
        stringline = stringline + " " + self.subtypestring + " "
        for string in self.argstringlist: #it's a list
            stringline = stringline + string + " "
        return stringline
    ################ All done ? ####################




            
