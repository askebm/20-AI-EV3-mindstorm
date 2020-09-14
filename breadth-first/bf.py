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

class Agent:
    def __init__(self,state):
        self.state=state

    def _isValidMove(self,delta):
        newpos = (self.state.pos[0]+delta[0],
                self.state.pos[1]+delta[1])
        futpos = (self.state.pos[0]+2*delta[0],
                self.state.pos[1]+2*delta[1])

        newfield = state.level[newpos[1]][newpos[0]] 
        futfield = state.level[futpos[1]][futpos[0]] 


        if (newfield in ' .') or (
                (newfield in r'$*') and (futfield in r' .')) :
            return True
        else:
            return False

    def generateStates(self):
        validMoves = [ m for m in [
            (1,0),(0,1),(-1,0),(0,-1)] if self._isValidMove(m)]
        result = []
        clearLevel = self.state.level
        if clearLevel[self.state.pos[1]][self.state.pos[0]] == r'@':
            clearLevel[self.state.pos[1]][self.state.pos[0]] = r' '
        else:
            clearLevel[self.state.pos[1]][self.state.pos[0]] = r'.'
        for m in validMoves:
            newpos = (self.state.pos[0]+m[0],
                    self.state.pos[1]+m[1])
            futpos = (self.state.pos[0]+2*m[0],
                    self.state.pos[1]+2*m[1])

            newLevel = clearLevel.copy()

            if clearLevel[newpos[1]][newpos[0]] ==  r' ':
                newLevel[newpos[1]][newpos[0]] = '@'
            elif clearLevel[newpos[1]][newpos[0]] == r'$':
                newLevel[newpos[1]][newpos[0]] = '@'
                if clearLevel[futpos[1]][futpos[0]] == r' ':
                    newLevel[futpos[1]][futpos[0]] = r'$'
                else:
                    newLevel[futpos[1]][futpos[0]] = r'*'
            elif clearLevel[newpos[1]][newpos[0]] ==  r'.':
                newLevel[newpos[1]][newpos[0]] = '+'
            elif clearLevel[newpos[1]][newpos[0]] == r'*':
                newLevel[newpos[1]][newpos[0]] = '+'
                if clearLevel[futpos[1]][futpos[0]] == r' ':
                    newLevel[futpos[1]][futpos[0]] = r'$'
                else:
                    newLevel[futpos[1]][futpos[0]] = r'*'
            State(newLevel,parent=self.state,pos=newpos)


## Initialise
LEVELS = json.load(open("../python-sokoban/levels.json"))

# hashmap for preventing doublicates
dPrevention = {}

## Test

state = State(LEVELS[0])
agent = Agent(state)
agent.generateStates()





