import sys
##
class Point:
    def __init__(self, x,y):
        self.x = x
        self.y = y
    def __str__(self):
        return "({0},{1})".format(self.x, self.y)

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Point(x, y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Point(x, y)

    def __eq__(self,other):
        return ( (self.x == other.x) and (self.y == other.y) )

##
class Level:
    def __init__(self,level):
        self.data = level.copy()
        self.boxes = []
        self.goals = []
        for y in range(len(level)):
            for x in range(len(level[y])):
                p = Point(x,y)
                if self[p] == '@':
                    self.player = Point(x,y)
                    self[p] = ' '
                elif self[p] == '+':
                    self.player = Point(x,y)
                    self.goals.append(Point(x,y))
                    self[p] = '.'
                elif self[p] == '$':
                    self.boxes.append(Point(x,y))
                    self[p] = ' '
                elif self[p] == '*':
                    self.boxes.append(Point(x,y))
                    self.goals.append(Point(x,y))
                    self[p] = '.'
                elif self[p] == '.':
                    self.goals.append(Point(x,y))



    def __getitem__(self,key):
        return self.data[key.y][key.x]
    def __setitem__(self,key,item):
        self.data[key.y][key.x] = item

#
# Tile   |   | Dock
# -------+---+-----
# Worker | @ | +
# Floor  |   | .
# Box    | $ | *
# Wall   | # | x
#


##
class Node:
    def __init__(self,boxes,position):
        self.boxes = boxes # [<Point>,...]
        self.position = position # <Point>
        self.connections = None # [(<Node>,<int>),...]

##
class Graph
    Wall = '#'
    moves = [Point(0,1),Point(1,0),Point(-1,0),Point(0,-1)]

    def __init__(self,root,level):
        self.root = root # <Node>
        self.level = level # [<string>,...]
        self.goal = None
        self.d = {} # {<string>:<Node>}

    def calcWeight(self,p1,p2,boxes):
        p = p2-p1
        return p.x**2+p.y**2

    def generateHash(self,boxes):
        level = Level(self.level.data.copy())
        for box in boxes:
            if level[box] == r' ':
                level[box] = r'$'
            else:
                level[box] = r'*'
        return "".join(level.data)


    def generate(self, node=self.root):
        for box in range(len(node.boxes)):
            for move in self.moves:
                newBox = move + node.boxes[box]
                if [True for p in node.boxes if p==newBox] and (level[newBox] != Wall):
                    newBoxes = node.boxes.copy()
                    newBoxes[box] = newBox
                    levelHash = sys.intern(self.generateHash(newBoxes))
                    weight = self.calcWeight(node.position,newBox,node.boxes)
                    recurse=False
                    if not self.d.get(levelHash,False):
                        self.d[levelHash] = Node(newBoxes,newBox)
                        recurse = True
                    self.d[levelHash].connections.append((node,weight))
                    node.connections.append((self.d[levelHash],weight))
                    if recurse:
                        self.generate(node.connections[-1][0])







