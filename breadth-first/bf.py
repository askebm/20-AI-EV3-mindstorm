## Imports

import anytree
import json

#
# Tile   |   | Dock
# -------+---+-----
# Worker | @ | +
# Floor  |   | .
# Box    | $ | *
# Wall   | # | x
#

## Define our nodes for breadth first

class State(anytree.NodeMixin):
    def __init__(self, level, parent=None, children=None,pos=None):
        self.level=level
        self.parent=parent
        if children:
            self.children=children
        self.dim = (len(level[0]),len(level))
        self.pos = pos if pos else ([ (x,y) for y in range(self.dim[1]) for x in range(self.dim[0]) if level[y][x]=='@'][0])
        

## Define agent for moving the map

class agent:
    def __init__(self,state):
        self.state=state

    def _isValidMove(delta):
        newpos = (self.state.pos[0]+delta[0],
                self.state.pos[1]+delta[1])
        futpos = (self.state.pos[0]+2*delta[0],
                self.state.pos[1]+2*delta[1])

        newfield = state.level[newpos[1]][newpos[0]] 
        futfield = state.level[futpos[1]][futpos[0]] 

        if (newfield in ' .') or (
                (newfield in r'$*') and (futfield in r' .')) :
            return true
        else
            return false

    def generateStates():
        validMoves = [m for m in [
            (1,0),(0,1),(-1,0),(0,-1)] if _isValidMove(m)]
        result = []
        clearLevel = self.state.level

        result = [ 




        


## Initialise
LEVELS = json.load(open("../python-sokoban/levels.json"))

# hashmap for preventing doublicates
dPrevention = {}

## 





