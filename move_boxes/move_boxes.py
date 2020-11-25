
import re
import copy
import numpy as np
from queue import PriorityQueue
import heapdict
import time
##

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
        self.order = None


    def c(self):
        n = Node()
        n.boxes = copy.deepcopy(self.boxes)
        n.player = copy.deepcopy(self.player)
        n.children = copy.copy(self.boxes)
        n.hash = copy.deepcopy(self.hash)
        n.parent = self.parent
        return n

##

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

    def is_solution(self,node):
        if self.solution == re.sub("M",".","".join(node.hash)):
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

    def is_deadlock(self,box):
        moves =[Position(1,0),Position(0,1)]

        for goal in self.goals:
            if goal == box:
                return False

        x_axis = self.level[box.y][box.x+1] + self.level[box.y][box.x-1]
        y_axis = self.level[box.y+1][box.x] + self.level[box.y-1][box.x]

        if "X" in x_axis and "X" in y_axis:
            return True

        return False
        

    def generate_children(self, node):

        if node.children:
            return
        
        moves =[Position(1,0),Position(0,1),Position(-1,0),Position(0,-1)]

        for move in moves:
            for box_i in range(len(node.boxes)):
                box = node.boxes[box_i]
                new_box = move + box
                if self.is_valid_move(box, move, node.hash) and \
                        not self.is_deadlock(new_box):
                    new_node = Node()
                    new_node.player = box
                    new_node.boxes = node.boxes[:box_i] + node.boxes[box_i+1:]
                    new_node.boxes.append(new_box)
                    new_node.hash = self.generate_hash(new_node)

                    h = "".join(new_node.hash)
                    if not self.nodes.get(h,False):
                        self.nodes[h] = new_node
                    else:
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
                #print(path__)
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

    def node_to_dot_string(self,node):
        return str(node.order) + r'\n' + r'\n'.join(node.hash)


    def to_dot(self,path):
        f = open(path,mode='w')
        f.write(r'digraph G {'+ "\n")
        f.write('graph [fontname = "monospace"];\n')
        f.write('node [fontname = "monospace"];\n')
        f.write('edge [fontname = "monospace"];\n')
        for node in self.nodes.values():
            for child_hash,path in node.children.items():
                child = self.nodes[child_hash]
                f.write(r'"' \
                        + self.node_to_dot_string(node) \
                        + r'" ->  "' \
                        + self.node_to_dot_string(child) \
                        + r'"' \
                        + r'[label="' + path + r'"];' \
                        + "\n")
        f.write(r'}')
        f.close()

    def a_star_global_heuristic(self,node):
        result = 0
        for box in node.boxes:
            dist = np.inf
            for g in self.goals:
                l = (g-box).norm()
                if l < dist:
                    dist = l
            result += dist
        return result 

    def a_star_global_reconstruct_path(self,cameFrom,current):
        total_path = [current]
        result = ""
        while current in cameFrom.keys():
            cF = cameFrom[current]
            current = cF
            total_path.insert(0,current)
        return total_path

    def a_star_global(self,max_iter=500):
        order = 0
        start = self.root
        start.order = order
        openSet = heapdict.heapdict()
        openSet[start] = self.a_star_global_heuristic(start)

        cameFrom = {}
        gScore = {}
        fScore = {}

        gScore[start] = 0

        fScore[start] = self.a_star_global_heuristic(start)

        while openSet.__len__() > 0:
            if max_iter == 0:
                print("Max iterations reached")
                return None
            max_iter -= 1
            current , current_score = openSet.popitem()
            if current.order is None:
                order += 1
                current.order = order

            if self.is_solution(current):
                print("A-star found a solution")
                return self.a_star_global_reconstruct_path(cameFrom,current)

            self.generate_children(current)
            for neighbor_hash in current.children:
                neighbor = self.nodes[neighbor_hash]
                tentative_gScore = gScore[current] + len(current.children[neighbor_hash])
                if tentative_gScore < gScore.get(neighbor,np.inf):
                    cameFrom[neighbor] = current
                    gScore[neighbor] = tentative_gScore
                    fScore[neighbor] = tentative_gScore + self.a_star_global_heuristic(neighbor)
                    if not openSet.get(neighbor):
                        openSet[neighbor] = fScore[neighbor]
        print("A-start did not find a solution")
        return None

    def create_solution_string(self,node_list):
        result = ""
        for i in range(len(node_list)-1):
            next_node_hash = "".join(node_list[i+1].hash)
            result += node_list[i].children[next_node_hash]
        return result





l = ["XXXXXXXXXXXX",
"XX...X.....X",
"XX...X.GG..X",
"XXJJJ.XGGXXX",
"X.J....MXXXX",
"X...X...XXXX",
"XXXXXXXXXXXX"]

l_yikes = [
"XXXXXXXXXXXXXXXXX",
"XXX..XXXXXXXXXXXX",
"X..GGX.XXXXXXXXXX",
"X.XGGX.X.....XXXX",
"X.XG.XXX...J....X",
"X.XG...X.J.J.JJ.X",
"X.X..M.XXX.JXX..X",
"X...........XXXXX",
"XX..XXXXXXXXXXXXX",
"XXXXXXXXXXXXXXXXX"
]

graph = Graph(l)

# print(graph.root.children)

#for node in graph.root.children:
#    print(node)
#    print(graph.root.children[node])

# for node in graph.nodes:
#     print(node)

solution = graph.a_star_global(max_iter=-1)
solution_string = graph.create_solution_string(solution)
print(solution_string)
graph.to_dot("graph.gv")
