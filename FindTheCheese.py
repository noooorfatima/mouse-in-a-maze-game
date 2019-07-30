"""

The main algorithm for the mouse in the maze should be written in this file

"""
# make Python look in the right place for logic.py
import sys
sys.path.append('/home/courses/python')
from logic import *
from Graphics import moveForward, turnLeft, turnRight, lookAhead, lookLeft, lookRight, eatCheese, mazeDebugOn, mazeDebugOff


def oneStepToCheese()-> None:
    
    #works by moving along the right wall    
  
    if lookRight()=="": #checking the right side first
       turnRight()
       moveForward()
    elif lookAhead()=="": #moving ahead
         moveForward()     
    elif lookLeft()=="": #moving left
         turnLeft()
         moveForward()
    else:
         turnLeft() #making a full turn if there is a dead end
         turnLeft()
         
      
                    
                
    


def moveToCheese()-> None:
    while lookAhead()!="c": #using while loop and calling upon onestepto cheese
          oneStepToCheese()
    eatCheese()
    print("Found the cheese!")
                      
            

def _test():
    import doctest
    result = doctest.testmod()
    if result[0] == 0:
        print("Wahoo! Passed all", result[1], __file__.split('/')[-1], "tests!")
    else:
        print("Rats!")

if __name__ == "__main__": _test()
