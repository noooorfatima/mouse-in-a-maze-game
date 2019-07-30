"""

THIS IS THE GRAPHICAL INTERFACE FOR THE MOUSE IN A MAZE PROJECT

IN CMSC 105, YOU DO NOT NEED TO READ OR UNDERSTAND IT.

"""

from tkinter import *
import random
import math
import time
import sys

class App:

    def __init__(self, master):
        self.size = 10
        self.mazeDebug = False
        self.mousePosition = (0,0)
        self.catPosition = (-1, -1)
        self.mouseDirection = "right"
        self.cheesePosition = (self.size-1,self.size-1)
        self.path = []
        
        self.multiplier = int(500/self.size)
        self.windowSize = self.multiplier*self.size
        self.maze = [[[1,1,0] for y in range(self.size)] for x in range(self.size)] # create a maze with no walls [right,bottom,ischeese]
        self.visited = []
        self.buildMaze()     
          
        self.frame = Frame(master)
        self.frame.pack()
        
        self.canvas = Canvas(self.frame, height=(self.windowSize+1), width=(self.windowSize+1), highlightthickness=0, cursor="crosshair")
        self.sideframe = Frame(self.frame, height=self.windowSize, width=200, bg="light blue")
        self.canvas.pack(side=LEFT)
        self.sideframe.pack(side=LEFT, expand=1, fill=BOTH)
        
        self.latest = 2
                
        self.displayMaze()
        self.displayMouse()
        self.displayCheese()
            
    def neighbors(self,x,y):
        temp = []
        if(x>0):
            temp.append((x-1,y))     
        if(y>0):
            temp.append((x,y-1))
        if(x<(self.size-1)):
            temp.append((x+1,y))     
        if(y<(self.size-1)):
            temp.append((x,y+1))
        return temp
        
    def deleteWallBetween(self,node1,node2):
        assert node1[0] == node2[0] or node1[1] == node2[1]
        if(node1[0] == node2[0]): 
            if(node1[1] > node2[1]):
                self.maze[node2[0]][node2[1]][1] = 0 # delete the bottom wall of the node closest to the top
            else:
                self.maze[node1[0]][node1[1]][1] = 0
        else: # node1[1] == node2[1]
            if(node1[0] > node2[0]):
                self.maze[node2[0]][node2[1]][0] = 0 # delete the right wall of the node closest to the left
            else:
                self.maze[node1[0]][node1[1]][0] = 0
            
    def buildMaze(self):
        pendingCells = [(0,0)]
        while(len(pendingCells)!=0):
            if(random.random()>0.2): # make the maze more random
                pointInList = int(random.random()*len(pendingCells))
                temp1 = pendingCells[0:pointInList]
                temp2 = pendingCells[pointInList:len(pendingCells)]
                temp1.reverse()
                pendingCells = temp1 + temp2
            x = pendingCells[-1][0]
            y = pendingCells[-1][1]
            neighbors = self.neighbors(x,y)
            if(len(neighbors)!=0):
                toBeDeleted = []
                for i in range(len(neighbors)):
                    if(neighbors[i] in self.visited):
                        toBeDeleted.append(neighbors[i])
                for i in toBeDeleted:
                    neighbors.remove(i)        
            if(len(neighbors)!=0):
                node = neighbors[int(random.random()*len(neighbors))]
                self.visited.append((x,y))
                pendingCells.append(node)
                self.deleteWallBetween((x,y),node)
            else:
                self.visited.append((x,y))
                pendingCells.remove((x,y))
                            
    def displayMaze(self):
        self.canvas.create_line([0,0,0,self.windowSize],fill="black")
        self.canvas.create_line([self.windowSize,0,self.windowSize,self.windowSize],fill="black")
        self.canvas.create_line([0,0,self.windowSize,0],fill="black")
        self.canvas.create_line([0,self.windowSize,self.windowSize,self.windowSize],fill="black")
        for x in range(len(self.maze)):
            for y in range(len(self.maze)):
                if(self.maze[x][y][0] == 1):
                    self.canvas.create_line([(x+1)*self.multiplier,y*self.multiplier,(x+1)*self.multiplier,(y+1)*self.multiplier],fill="black")
                if(self.maze[x][y][1] == 1):
                    self.canvas.create_line([x*self.multiplier,(y+1)*self.multiplier,(x+1)*self.multiplier,(y+1)*self.multiplier],fill="black")

    def displayMouse(self):
        self.photo = PhotoImage(file="mouse.gif")
        self.photo = self.photo.zoom(25)
        self.photo = self.photo.subsample(self.size*2+4)
        
        self.photoup = PhotoImage(file="mouseup.gif")
        self.photoup = self.photoup.zoom(25)
        self.photoup = self.photoup.subsample(self.size*2+4)
        
        self.photoleft = PhotoImage(file="mouseleft.gif")
        self.photoleft = self.photoleft.zoom(25)
        self.photoleft = self.photoleft.subsample(self.size*2+4)
        
        self.photodown = PhotoImage(file="mousedown.gif")
        self.photodown = self.photodown.zoom(25)
        self.photodown = self.photodown.subsample(self.size*2+4)
        
        self.item = self.canvas.create_image(self.mousePosition[0]*self.multiplier+1, self.mousePosition[1]*self.multiplier, anchor=NW, image=self.photo)
        
    def displayCheese(self):    
        self.photo2 = PhotoImage(file="cheese.gif")
        self.photo2 = self.photo2.zoom(25)
        self.photo2 = self.photo2.subsample(self.size*2)
        
        self.item2 = self.canvas.create_image(self.cheesePosition[0]*self.multiplier, self.cheesePosition[1]*self.multiplier, anchor=NW, image=self.photo2)
        self.canvas.tag_lower(self.item2)
    
    def updateMousePosition(self):
        self.canvas.coords(self.item,self.mousePosition[0]*self.multiplier+1, self.mousePosition[1]*self.multiplier)
    
    def updateMouseRotation(self):
        self.canvas.delete(self.item)
        if(app.mouseDirection == "right"):
            self.item = self.canvas.create_image(self.mousePosition[0]*self.multiplier, self.mousePosition[1]*self.multiplier+1, anchor=NW, image=self.photo)
        elif(app.mouseDirection == "left"):
            self.item = self.canvas.create_image(self.mousePosition[0]*self.multiplier, self.mousePosition[1]*self.multiplier+1, anchor=NW, image=self.photoleft)
        elif(app.mouseDirection == "up"):
            self.item = self.canvas.create_image(self.mousePosition[0]*self.multiplier, self.mousePosition[1]*self.multiplier+1, anchor=NW, image=self.photoup)
        elif(app.mouseDirection == "down"):
            self.item = self.canvas.create_image(self.mousePosition[0]*self.multiplier, self.mousePosition[1]*self.multiplier+1, anchor=NW, image=self.photodown)
        root.update_idletasks()
    
    def clearMaze(self):
        stufftoclear = self.canvas.find_all()
        for i in stufftoclear:
            self.canvas.delete(i)
            
    def restartMaze(self):
        app.mousePosition = (0,0)
        app.mouseDirection = "right"
        app.cheesePosition = (app.size-1,app.size-1)
        app.path = []
        app.visited = []
        app.canvas.delete("line")
        app.displayMouse()
        app.displayCheese()  
        
    def catAttack(self):
        print("Oh, no! The cat!")
        self.cat = PhotoImage(file="cat.gif")
        self.item8 = self.canvas.create_image(self.mousePosition[0]*self.multiplier-60, self.mousePosition[1]*self.multiplier-60, anchor=NW, image=self.cat)
        root.updateIdletasks()
        time.sleep(2)
        self.canvas.delete(self.item8)
        self.mousePosition = self.catPosition
        self.updateMousePosition()
        sys.exit()
            
root = Tk()

app = App(root)

def mazeDebugOn():
    app.mazeDebug = True

def mazeDebugOff():
    app.mazeDebug = False

def mazeDebug(string):
    if (app.mazeDebug):
        print(string)
        
def mazePrint(string):
    print(string)

def turnLeft()-> None:
    mazeDebug("Turning left")
    if(app.mouseDirection == "right"):
        app.mouseDirection = "up"
    elif(app.mouseDirection == "left"):
        app.mouseDirection = "down"
    elif(app.mouseDirection == "up"):
        app.mouseDirection = "left"
    elif(app.mouseDirection == "down"):
        app.mouseDirection = "right"
    app.updateMouseRotation()   
    
def turnRight()-> None:
    mazeDebug("Turning right")
    if(app.mouseDirection == "right"):
        app.mouseDirection = "down"
    elif(app.mouseDirection == "left"):
        app.mouseDirection = "up"
    elif(app.mouseDirection == "up"):
        app.mouseDirection = "right"
    elif(app.mouseDirection == "down"):
        app.mouseDirection = "left"
    app.updateMouseRotation()

def whatIsAhead():
    if (app.mousePosition == app.catPosition):
        return "cat's stomach"
    elif (app.mousePosition == app.cheesePosition):
        return "c"
    else:
        if(app.mouseDirection == "right"):
            if(app.mousePosition[0] >= (app.size-1) or app.maze[app.mousePosition[0]][app.mousePosition[1]][0] == 1):
                return "w"
            else:
                return ""
        elif(app.mouseDirection == "left"):
            if(app.mousePosition[0] <= 0 or app.maze[app.mousePosition[0]-1][app.mousePosition[1]][0] == 1):
                return "w"
            else:
                return ""
        elif(app.mouseDirection == "up"):
            if(app.mousePosition[1] <= 0 or app.maze[app.mousePosition[0]][app.mousePosition[1]-1][1] == 1):
                return "w"
            else:
                return ""
        elif(app.mouseDirection == "down"):
            if(app.mousePosition[1] >= (app.size-1) or app.maze[app.mousePosition[0]][app.mousePosition[1]][1] == 1):
                return "w"
            else:
                return ""

def whatIsRight():
    if (app.mousePosition == app.catPosition):
        return "cat's stomach"
    elif (app.mousePosition == app.cheesePosition):
        return "c"
    else:
        if(app.mouseDirection == "up"):
            if(app.mousePosition[0] >= (app.size-1) or app.maze[app.mousePosition[0]][app.mousePosition[1]][0] == 1):
                return "w"
            else:
                return ""
        elif(app.mouseDirection == "down"):
            if(app.mousePosition[0] <= 0 or app.maze[app.mousePosition[0]-1][app.mousePosition[1]][0] == 1):
                return "w"
            else:
                return ""
        elif(app.mouseDirection == "left"):
            if(app.mousePosition[1] <= 0 or app.maze[app.mousePosition[0]][app.mousePosition[1]-1][1] == 1):
                return "w"
            else:
                return ""
        elif(app.mouseDirection == "right"):
            if(app.mousePosition[1] >= (app.size-1) or app.maze[app.mousePosition[0]][app.mousePosition[1]][1] == 1):
                return "w"
            else:
                return ""
                
def whatIsLeft():
    if (app.mousePosition == app.catPosition):
        return "cat's stomach"
    elif (app.mousePosition == app.cheesePosition):
        return "c"
    else:
        if(app.mouseDirection == "down"):
            if(app.mousePosition[0] >= (app.size-1) or app.maze[app.mousePosition[0]][app.mousePosition[1]][0] == 1):
                return "w"
            else:
                return ""
        elif(app.mouseDirection == "up"):
            if(app.mousePosition[0] <= 0 or app.maze[app.mousePosition[0]-1][app.mousePosition[1]][0] == 1):
                return "w"
            else:
                return ""
        elif(app.mouseDirection == "right"):
            if(app.mousePosition[1] <= 0 or app.maze[app.mousePosition[0]][app.mousePosition[1]-1][1] == 1):
                return "w"
            else:
                return ""
        elif(app.mouseDirection == "left"):
            if(app.mousePosition[1] >= (app.size-1) or app.maze[app.mousePosition[0]][app.mousePosition[1]][1] == 1):
                return "w"
            else:
                return ""
            
def lookAhead()-> str:
    result = whatIsAhead()
    mazeDebug("Looking ahead ... seeing " + result)
    return result

def lookRight()-> str:
    result = whatIsRight()
    mazeDebug("Looking right ... seeing " + result)
    return result

def lookLeft()-> str:
    result = whatIsLeft()
    mazeDebug("Looking left ... seeing " + result)
    return result

def moveForward()-> None:
    if(whatIsAhead() != "w" and whatIsAhead() != "cat's stomach"):
        mazeDebug("Moving forward")
        oldPosition = app.mousePosition
        if(app.mouseDirection == "right"):
            app.mousePosition = (app.mousePosition[0]+1,app.mousePosition[1])
        elif(app.mouseDirection == "left"):
            app.mousePosition = (app.mousePosition[0]-1,app.mousePosition[1])
        elif(app.mouseDirection == "up"):
            app.mousePosition = (app.mousePosition[0],app.mousePosition[1]-1)
        elif(app.mouseDirection == "down"):
            app.mousePosition = (app.mousePosition[0],app.mousePosition[1]+1)
        app.updateMousePosition()    
        if((app.mousePosition,oldPosition) in app.path):
            app.canvas.delete(app.latest)
            app.path.remove((app.mousePosition,oldPosition))
            app.canvas.create_line([oldPosition[0]*app.multiplier + int(app.multiplier/2),oldPosition[1]*app.multiplier + int(app.multiplier/2),app.mousePosition[0]*app.multiplier + int(app.multiplier/2),app.mousePosition[1]*app.multiplier + int(app.multiplier/2)],fill="yellow",tags="line")
        else:
            app.latest = app.canvas.create_line([oldPosition[0]*app.multiplier + int(app.multiplier/2),oldPosition[1]*app.multiplier + int(app.multiplier/2),app.mousePosition[0]*app.multiplier + int(app.multiplier/2),app.mousePosition[1]*app.multiplier + int(app.multiplier/2)],fill="red",tags="line")
            app.path.append((oldPosition,app.mousePosition))
    elif (whatIsAhead() == "w"):
        mazePrint("Trying to move through a wall!")
        app.catAttack()
    # else do nothing!
    root.update_idletasks()
    
def eatCheese()-> bool:
    if(whatIsAhead()=="c"):
        mazePrint("Eating cheese ... yum yum!")
        return True
    else:
        mazePrint("Trying to eat cheese when there's none there!")
        app.catAttack()
        return False
