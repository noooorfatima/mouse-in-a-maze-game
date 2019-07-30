"""

THIS IS THE "GET THINGS STARTED" FILE FOR THE MOUSE IN A MAZE PROJECT

IN CMSC 105, YOU SHOULD RUN THIS FILE, BUT DO NOT NEED TO READ OR UNDERSTAND IT.

"""


from Graphics import *
from FindTheCheese import *

# Hopefully the following will stop any infinite loops without killing anything correct
import resource
resource.setrlimit(resource.RLIMIT_CPU, [30, 35])


def generateMaze():
    app.size = int(entry2.get())
    app.maze = [[[1,1,0] for y in range(app.size)] for x in range(app.size)]
    app.mousePosition = (0,0)
    app.mouseDirection = "right"
    app.cheesePosition = (app.size-1,app.size-1)
    app.path = []
        
    app.multiplier = int(500/app.size)
    app.windowSize = app.multiplier*app.size
    app.maze = [[[1,1,0] for y in range(app.size)] for x in range(app.size)] # create a maze with no walls [right,bottom,ischeese]
    app.visited = []
    app.clearMaze()
    app.buildMaze()
    app.displayMaze()
    app.displayMouse()
    app.displayCheese()  

button1 = Button(app.sideframe, text="Do 1 Step", highlightbackground="light blue", command=oneStepToCheese)
button2 = Button(app.sideframe, text="Find the Cheese!", highlightbackground="light blue", command=moveToCheese)
button3 = Button(app.sideframe, text="Generate New Maze!", highlightbackground="light blue", command=generateMaze)
button4 = Button(app.sideframe, text="Reset Mouse and Cheese", highlightbackground="light blue", command=app.restartMaze)
# button5 = Button(app.sideframe, text="Eat the mouse", highlightbackground="light blue", command=app.catAttack)
buttonDebugOn = Button(app.sideframe, text="Debugging output ON", highlightbackground="light blue", command=mazeDebugOn)
buttonDebugOff = Button(app.sideframe, text="Debugging output OFF", highlightbackground="light blue", command=mazeDebugOff)

v2 = StringVar()
v2.set("10")

frame2 = Frame(app.sideframe, bg="light blue")
label2 = Label(frame2, text="size of maze:", bg="light blue")
entry2 = Entry(frame2, textvariable=v2, width=3, highlightbackground="light blue")

button1.pack(side=TOP, anchor=W)
button2.pack(side=TOP, anchor=W)
button4.pack(side=TOP, anchor=W)
buttonDebugOn.pack(side=TOP, anchor=W)
buttonDebugOff.pack(side=TOP, anchor=W)
frame2.pack(side=TOP, anchor=W)
label2.pack(side=LEFT)
entry2.pack(side=LEFT)
button3.pack(side=TOP, anchor=W)
# button5.pack(side=TOP, anchor=W)

root.mainloop()