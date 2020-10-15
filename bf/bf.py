#!/usr/bin/python3
import re
import copy


##


class Position():

    def __init__(self,x,y):
        self.x = x
        self.y = y

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

##

class Node():
    def __init__(self):
        self.boxes = []
        self.player = None
        self.children = []
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


##
class Tree():
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

    def generate_children(self,node):
#        print("I wanna make children")
        moves =[Position(1,0),Position(0,1),Position(-1,0),Position(0,-1)]
        for p in moves:
            new_player = p+node.player
            behind_box = new_player + p
            n = None
            
            if (node.hash[new_player.y][new_player.x] == "."): 
                n = Node()
                n.player = new_player
                n.boxes = node.boxes
            elif ( node.hash[new_player.y][new_player.x] == "J" and
                        (node.hash[behind_box.y][behind_box.x] == ".")):

                wall_counter = 0
                if not [True for g in self.goals if behind_box == g]:
                    for move in moves:
                        maybe_wall = move + behind_box
                        if self.level[maybe_wall.y][maybe_wall.x] == "X":
                            wall_counter +=1

                if wall_counter <= 1:
                    n = Node()
                    n.player = new_player
                    n.boxes = []
                    for bi in node.boxes:
                        if new_player == bi:
                            n.boxes.append(behind_box)
                        else:
                            n.boxes.append(bi)
            
            if n != None:
#                print("I made a child")
                n.hash = self.generate_hash(n)
                h = "".join(n.hash)
                if not self.nodes.get(h,False):
                    self.nodes[h] = n
                    node.children.append(self.nodes[h])
                    n.parent = node
#                nodes[n.hash].children.append(node)

    def bf_search(self,max_iter=500):
        for d in range(max_iter):
            result = self._bf_search(self.root,depth=d)
            if result != None:
                print("Solution found")
                return result
        print("No solution found")
        return None
        

    def _bf_search(self,node,depth=1):
        if depth == 0:
            self.generate_children(node)
#            print("Generated " + str(len(node.children)) +" children")
            for child in node.children:
                result = True
                if self.isSolution("".join(child.hash)):
                    return child
            return None
        else:
            for n in node.children:
                 res = self._bf_search(n,depth-1)
                 if res != None:
                     return res
            return None

    def to_dot(self,path):
        f = open(path,mode='w')
        f.write(r'digraph G {'+ "\n")
        f.write('graph [fontname = "monospace"];\n')
        f.write('node [fontname = "monospace"];\n')
        f.write('edge [fontname = "monospace"];\n')
        self._to_dot(f,self.root)
        f.write(r'}')
        f.close()
    
    def _to_dot(self,f,node):
        f.write(r'"' + r'\n'.join(node.hash) + r'"'+ "\n")
        if node.parent != None:
            f.write(r'"' + r'\n'.join(node.parent.hash) + r'" ->  "' + r'\n'.join(node.hash) + r'"'+ "\n")
        for child in node.children:
            self._to_dot(f,child)


    def layer_to_dot(self,path,layer):
        f = open(path,mode='w')
        f.write(r'digraph G {'+ "\n")
        f.write('graph [fontname = "monospace"];\n')
        f.write('node [fontname = "monospace"];\n')
        f.write('edge [fontname = "monospace"];\n')
        self._layer_to_dot(f,self.root,layer)
        f.write(r'}')
        f.close()

    def _layer_to_dot(self,f,node,layer):
        if layer == 0:
            f.write(r'"' + r'\n'.join(node.hash) + r'"'+ "\n")
        else:
            for child in node.children:
                self._layer_to_dot(f,child,layer-1)

    def generate_path(self,node):
        parent = node.parent
        result = ""
        while parent != None:
            delta_move = node.player - parent.player
            instruction = ""
            if delta_move.x == -1:
                instruction = "l"
            elif delta_move.x == 1: 
                instruction = "r"
            elif delta_move.y == 1: 
                instruction = "d"
            elif delta_move.y == -1: 
                instruction = "u"

            if node.boxes != parent.boxes:
                instruction = instruction.upper()
            result = instruction + result

            node = parent
            parent = node.parent


        return result






##

l = ["XXXXXXXXXXXX",
"XX...X.....X",
"XX...X.GG..X",
"XXJJJ.XGGXXX",
"X.J....MXXXX",
"X...X...XXXX",
"XXXXXXXXXXXX"]

##

t = Tree(l)
solution = t.bf_search(max_iter=140)

##

t.generate_path(solution)

##
t.layer_to_dot("layer.gv",108)
print("Done")

##
t.to_dot("dot2.gv")
print("Done")


