
import re
import copy
import numpy as np
from queue import PriorityQueue
import heapdict
import time


class Position():

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.hash = self.__hash__()

    def __add__(self,other):
        y = self.y + other.y
        x = self.x + other.x
        return Position(x,y)

    def __sub__(self,other):
        y = self.y - other.y
        x = self.x - other.x
        return Position(x,y)

    def __eq__(self,other):
        return ( (self.x == other.x) and (self.y == other.y) )

    def __deepcopy_(self):
        return Position(self.x.deepcopy(),self.y.deepcopy())

    def norm(self):
        return np.sqrt(self.x**2+self.y**2)

    def manhatten_distance(self):
        return abs(self.x) + abs(self.y)

    def __hash__(self):
        return 1000*self.x + self.y

##

class Node():
    def __init__(self):
        self.boxes = []
        self.player = None
        self.children = {}
        self.hash = None
        self.parent = None

    def c(self):
        n = Node()
        n.boxes = copy.deepcopy(self.boxes)
        n.player = copy.deepcopy(self.player)
        n.children = copy.copy(self.boxes)
        n.hash = copy.deepcopy(self.hash)
        n.parent = self.parent
        return n



class Graph():
    def __init__(self,level):
        self.goals = []
        self.root = Node()
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == "M":
                    self.root.player = Position(x,y)
                elif level[y][x] == "J":
                    self.root.boxes.append(Position(x,y))
                elif level[y][x] == "G":
                    self.goals.append(Position(x,y))

        

        self.solution = [ re.sub("[JM]",".",i) for i in level ]
        self.solution = [ re.sub("G","J",i) for i in self.solution ]
        self.solution = "".join(self.solution)
        self.level = [ re.sub("[MJG]",".",i) for i in level ]
        self.root.hash = [ re.sub("G",".",i) for i in level ]
        self.nodes = {"".join(self.root.hash):self.root}
    def number_of_nodes(self):
        return len(self.nodes)

    def max_depth(self):
        node = self.nodes[list(self.nodes)[-1]]
        cnt = 1
        while node.parent != None:
            cnt += 1
            node = node.parent
        return cnt

    def isSolution(self,joined_hash):
        if self.solution == re.sub("M",".",joined_hash):
            return True
        else:
            return False


    def generate_hash(self,node):
        result = copy.deepcopy(self.level)
        for b in node.boxes:
            result[b.y] = result[b.y][:b.x] + "J" + result[b.y][b.x+1:]
        result[node.player.y] = result[node.player.y][:node.player.x] + "M" + \
                result[node.player.y][node.player.x+1:]
        return result

    def is_valid_move(self,box,move,level):
        p = box - move
        nb = box + move
        clear = level[p.y][p.x] + level[nb.y][nb.x]
        for obstacle in "JX":
            if obstacle in clear:
                return False
        return True

    def generate_children(self, node):
        
        moves =[Position(1,0),Position(0,1),Position(-1,0),Position(0,-1)]

        for move in moves:
            for box_i in range(len(node.boxes)):
                box = node.boxes[box_i]
                new_box = move + box
                if self.is_valid_move(box, move, node.hash):
                    new_node = Node()
                    new_node.player = box
                    new_node.boxes = node.boxes[:box_i] + node.boxes[box_i+1:]
                    new_node.boxes.append(new_box)
                    new_node.hash = self.generate_hash(new_node)

                    h = "".join(new_node.hash)
                    if not self.nodes.get(h,False):
                        self.nodes[h] = new_node

                    new_node = self.nodes[h]

                    path = self.a_star(node, new_node, move)

                    if path is not None:
                        if not node.children.get(h, False):
                            node.children[h] = path
                    
        return 



    def a_star_reconstruct_path(self,cameFrom,current):
        total_path = [current]
        result = ""
        while current in cameFrom.keys():

            cF = cameFrom[current]
            delta_move = current - cF
            instruction = ""
            if delta_move.x == -1:
                instruction = "l"
            elif delta_move.x == 1: 
                instruction = "r"
            elif delta_move.y == 1: 
                instruction = "d"
            elif delta_move.y == -1: 
                instruction = "u"

            result = instruction + result

            current = cF
            total_path.insert(0, current)
        
        return result

    

    def a_star_heuristic(self, current, end):
        manhatten = end - current
        return manhatten.manhatten_distance()


    def a_star(self, start_node, end_node, move, max_iter=500):
        start = start_node.player
        end = end_node.player - move
        openSet = heapdict.heapdict()
        openSet[start] = self.a_star_heuristic(start, end)
        level = start_node.hash

        cameFrom = {}
        gScore = {}
        fScore = {}

        gScore[start] = 0

        fScore[start] = self.a_star_heuristic(start, end)

        while openSet.__len__() > 0:
            max_iter -= 1
            current , current_score = openSet.popitem()
            instruction = ""
            if current == end:
                if move.x == -1:
                    instruction = "L"
                elif move.x == 1: 
                    instruction = "R"
                elif move.y == 1: 
                    instruction = "D"
                elif move.y == -1: 
                    instruction = "U"
                path__ = self.a_star_reconstruct_path(cameFrom,current) + instruction
                print(path__)
                return self.a_star_reconstruct_path(cameFrom,current) + instruction

            moves =[Position(1,0),Position(0,1),Position(-1,0),Position(0,-1)]
            for p in moves:
                neighbor = current + p
                c = level[neighbor.y][neighbor.x]
                if c == "." or c == "G":
                    tentative_gScore = gScore[current] + 1
                    if tentative_gScore < gScore.get(neighbor,np.inf):
                        cameFrom[neighbor] = current
                        gScore[neighbor] = tentative_gScore
                        fScore[neighbor] = tentative_gScore + self.a_star_heuristic(neighbor, end)
                        if not openSet.get(neighbor):
                            openSet[neighbor] = fScore[neighbor]
        return None


    def to_dot(self,path):
        f = open(path,mode='w')
        f.write(r'digraph G {'+ "\n")
        f.write('graph [fontname = "monospace"];\n')
        f.write('node [fontname = "monospace"];\n')
        f.write('edge [fontname = "monospace"];\n')
        self._to_dot(f, self.root)
        f.write(r'}')
        f.close()
    
    def _to_dot(self, f, node, parent=None, path=""):
        f.write(r'"' + r'\n'.join(node.hash) + r'"'+ "\n")
        if parent != None:
            f.write(r'"' + r'\n'.join(parent.hash) + r'" ->  "' + r'\n'.join(node.hash) + r'"' + r'[label="' + path + r'"];' + "\n")
        for child in node.children:
            self._to_dot(f, self.nodes[child], parent = node, path = node.children[child])





l = ["XXXXXXXXXXXX",
"XX...X.....X",
"XX...X.GG..X",
"XXJJJ.XGGXXX",
"X.J....MXXXX",
"X...X...XXXX",
"XXXXXXXXXXXX"]

graph = Graph(l)

graph.generate_children(graph.root)

# print(graph.root.children)

for node in graph.root.children:
    print(node)
    print(graph.root.children[node])

# for node in graph.nodes:
#     print(node)

graph.to_dot("graph.gv")