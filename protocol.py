import pygame, sys, random

class Protocol(object):
    def __init__(self, robot):
        self.next = None
        self.top = 0
        self.robot = robot
        self.name = ""
    def addCommand(self, command):
        command.setIndex(len(commands))
        self.commands.append(command)
    def nameProtocol(self, name):
        self.name = name
    def removeCommand(self, command):
        commands.pop(command.index)
    def perform(self):
        ret = self.commands[self.step].perform()
        if ret == 1:
            self.step += 1
        if self.top == len(self.commands):		#The protocol has finished
            return 1
        return 0
    def saveProtocol(self, filename):
        f = open(filename, 'w')
        for command in commands:
            f.write(command.name+'\n')
            f.close()
class forLoop(protocol):
	def __init__(self, robot):
		protocol.__init__(self, robot)
		self.size = 0
		self.pos = 0
	def setSize(self, newsize):
		self.size = newsize
	def perform(self):
		ret = super(forLoop, self).perform()
		if ret == 1:
			self.pos +=1
			if self.size == self.pos:
				return 1
		return 0
class IfStatement(protocol):
	def __init__(self, robot):
		protocol.__init__(self, robot)
		self.type = None 
		self.A = None
		self.B = None
	def setA(self, A):
		self.A = A
	def setB(self, B):
		self.B = B
	def setType(self, type):
		self.type = type  		#(0, =), (1, >), (2, <), (3, <=), (4, >=), (5, !=)
	def compareValues(self):
		if type == 0:
			if A == B:
				return 1
		elif type == 1:
			if A > B:
				return 1
		elif type == 2:
			if A < B:
				return 1
		elif type == 3:
			if A<= B:
				return 1
		elif type == 4:
			if A >= B:
				return 1
		elif type == 5:
			if A!= B:
				return 1
		return 0
	def perform(self):
		ret = compareValues()
		if ret == 1:
			super(IfStatement, self).perform()
		else:
			return -1
			
#While is more complicated because we will need comparisons similar to those in If

		
		
	
