#!/usr/bin/env python3

# Test if imports work
print("starting now")
from CatanGame.Tile import Tile
from CatanGame.Node import Node
from CatanGame.Board import Board
import random
import networkx as nx
G = nx.Graph()
nodemap = {}
tilemaplist = [{0:1, 240: 3, 300: 4},
           {0: 2, 180: 0, 240: 4, 300: 5},
           {180: 1, 240: 5, 300: 6},
           {0:4, 60: 0, 240: 7, 300: 8},
           {0:5, 60:1, 120:0, 180:3, 240: 8, 300: 9},
           {0:6, 60: 2, 120: 1, 180: 4, 240: 9, 300: 10},
           {120:2, 180:5, 240:10, 300:11},
           {0:8, 60:3,300:12},
           {0:9, 60:4, 120:3, 180:7, 240:12,300:13},
           {0:10, 60:5, 120:4, 180:8, 240:13, 300:14},
           {0:11, 60:6, 120:5, 180:9, 240:14, 300:15},
           {120:6, 180: 10, 240:15},
           {0:13, 60:8,120:7,300:16},
           {0:14, 60:9, 120:8,180:12,240:16, 300:17},
           {0:15, 60:10, 120:9, 180:13, 240:17, 300:18},
           {60:11, 120:10, 180:14, 240:18},
           {0:17, 60:13, 120:12},
           {0:18, 60:14, 120:13, 180:16},
           {60:15, 120:14, 180:17}]
resources = ["rock"] * 3 + ["mud"] * 3 + ["wheat"] * 4 + ["tree"] * 4 + ["sheep"] * 4
random.shuffle(resources)
numbers = [3, 4, 5, 6, 8, 9, 10, 11] * 2 + [2, 12]
random.shuffle(numbers)
interval = random.randint(0, 19)
resources = resources[0:interval] + ['desert'] + resources[interval:]
numbers = numbers[0:interval] + [-1] + numbers[interval:]


class dummyboard:
    G = nx.Graph()
    nodemap = {}
    tilemaplist = [{0:1, 240: 3, 300: 4},
            {0: 2, 180: 0, 240: 4, 300: 5},
            {180: 1, 240: 5, 300: 6},
            {0:4, 60: 0, 240: 7, 300: 8},
            {0:5, 60:1, 120:0, 180:3, 240: 8, 300: 9},
            {0:6, 60: 2, 120: 1, 180: 4, 240: 9, 300: 10},
            {120:2, 180:5, 240:10, 300:11},
            {0:8, 60:3,300:12},
            {0:9, 60:4, 120:3, 180:7, 240:12,300:13},
            {0:10, 60:5, 120:4, 180:8, 240:13, 300:14},
            {0:11, 60:6, 120:5, 180:9, 240:14, 300:15},
            {120:6, 180: 10, 240:15},
            {0:13, 60:8,120:7,300:16},
            {0:14, 60:9, 120:8,180:12,240:16, 300:17},
            {0:15, 60:10, 120:9, 180:13, 240:17, 300:18},
            {60:11, 120:10, 180:14, 240:18},
            {0:17, 60:13, 120:12},
            {0:18, 60:14, 120:13, 180:16},
            {60:15, 120:14, 180:17}]
    resources = ["rock"] * 3 + ["mud"] * 3 + ["wheat"] * 4 + ["tree"] * 4 + ["sheep"] * 4
    #random.shuffle(resources)
    numbers = [3, 4, 5, 6, 8, 9, 10, 11] * 2 + [2, 12]
    #random.shuffle(numbers)
    #interval = random.randint(0, 19)
    #resources = resources[0:interval] + ['desert'] + resources[interval:]
    #numbers = numbers[0:interval] + [-1] + numbers[interval:]

    tiles = []
    for i in range(5):
        tiles.append(Tile(resource=resources.pop(), number = numbers.pop(), G = G))
    # Make a map that points to a node based off the unique id of a node. 
    for i in range(len(tiles)):
        for j in range(len(tiles[i].nodes)):
            if (i, j) not in nodemap:
                nodemap[(i,j)] = tiles[i].nodes[j]
    # (0,0) would be the node at the 0th tile 30 degrees above.
    def __init__(self):
        self.join0(self.tiles[0], self.tiles[1], self.tiles)
        self.join60(self.tiles[3], self.tiles[0], self.tiles)
        self.join120(self.tiles[4], self.tiles[0], self.tiles)
        self.join0(self.tiles[3], self.tiles[4], self.tiles)
        self.join60(self.tiles[4], self.tiles[2], self.tiles)
        return

    # When Tile A is to the left of Tile B
    def join0(self,  a: Tile, b: Tile, Tiles):
        idx_b = Tiles.index(b)
        tmp1 = b.nodes[2]
        tmp2 = b.nodes[3]

        neighbors1 = list(self.G.neighbors(tmp1))
        neighbors2 = list(self.G.neighbors(tmp2))

        self.G.remove_node(tmp1)
        self.G.remove_node(tmp2)


        b.nodes[2] = a.nodes[0]
        self.nodemap[(idx_b, 2)] = a.nodes[0]
        for tile in Tiles:
            for i in range(len(tile.nodes)):
                if tile.nodes[i] is tmp1:
                    tile.nodes[i] = a.nodes[0]
                    # Get the idx of that tile and the idx of that node
                    tmp_idx = Tiles.index(tile)
                    self.nodemap[(tmp_idx, i)] = a.nodes[0]
        for neighbor in neighbors1:
            if neighbor in self.G:
                self.G.add_edge(a.nodes[0], neighbor, owner = None, roadowner = None)

        b.nodes[3] = a.nodes[5]
        self.nodemap[(idx_b, 3)] = a.nodes[5]
        for tile in Tiles:
            for i in range(len(tile.nodes)):
                if tile.nodes[i] is tmp2:
                    tile.nodes[i] = a.nodes[5]
                    tmp_idx = Tiles.index(tile)
                    self.nodemap[(tmp_idx, i)] = a.nodes[5]
        for neighbor in neighbors2:
            if neighbor in self.G:
                self.G.add_edge(a.nodes[5], neighbor, owner = None, roadowner = None)
        

        #b.nodes[2].resources = list(set(b.nodes[2].resources + tmp1.resources))
        b.nodes[2].resources[2] = b.resource
        b.nodes[2].resources[1] = a.resource
        #b.nodes[2].numbers = list(set(b.nodes[2].numbers + tmp1.numbers))
        b.nodes[2].numbers[2] = b.number
        b.nodes[2].numbers[1] = a.number
        
        #b.nodes[3].resources = list(set(b.nodes[3].resources + tmp2.resources))
        b.nodes[3].resources[0] = a.resource
        b.nodes[3].resources[1] = b.resource
        #b.nodes[3].numbers = list(set(b.nodes[3].numbers + tmp2.numbers))
        b.nodes[3].numbers[0] = a.number
        b.nodes[3].numbers[1] = b.number

        return

    def join60(self, a: Tile, b: Tile, Tiles):
        idx_b = Tiles.index(b)

        neighbors1 = list(self.G.neighbors(b.nodes[3]))
        neighbors2 = list(self.G.neighbors(b.nodes[4]))
        
        self.G.remove_node(b.nodes[3])
        self.G.remove_node(b.nodes[4])
        
        tmp1 = b.nodes[3]
        tmp2 = b.nodes[4]
        
        b.nodes[3] = a.nodes[1]
        self.nodemap[(idx_b, 3)] = a.nodes[1]
        for tile in Tiles:
            for i in range(len(tile.nodes)):
                if tile.nodes[i] is tmp1:
                    tile.nodes[i] = a.nodes[1]
                    tmp_idx = Tiles.index(tile)
                    self.nodemap[(tmp_idx, i)] = a.nodes[1]

        for neighbor in neighbors1:
            if neighbor in self.G:
                self.G.add_edge(b.nodes[3], neighbor, owner = None, roadowner = None)
        
        b.nodes[4] = a.nodes[0]
        self.nodemap[(idx_b, 4)] = a.nodes[0]
        for tile in Tiles:
            for i in range(len(tile.nodes)):
                if tile.nodes[i] is tmp2:
                    tile.nodes[i] = a.nodes[0]
                    tmp_idx = Tiles.index(tile)
                    self.nodemap[(tmp_idx, i)] = a.nodes[0]
        for neighbor in neighbors2:
            if neighbor in self.G:
                self.G.add_edge(b.nodes[4], neighbor, owner = None, roadowner = None)

        #a.nodes[1].resources = list(set(a.nodes[1].resources + tmp1.resources))
        a.nodes[1].resources[1] = b.resource
        a.nodes[1].resources[2] = a.resource
        #a.nodes[1].numbers = list(set(a.nodes[1].numbers + tmp1.numbers))  
        a.nodes[1].numbers[1] = b.number
        a.nodes[1].numbers[2] = a.number

        #a.nodes[0].resources = list(set(a.nodes[0].resources + tmp2.resources))
        a.nodes[0].resources[0] = b.resource
        a.nodes[0].resources[1] = a.resource
        #a.nodes[0].numbers = list(set(a.nodes[0].numbers + tmp2.numbers))
        a.nodes[0].numbers[0] = b.number
        a.nodes[0].numbers[1] = a.number
        return

    def join120(self, a: Tile, b: Tile, Tiles):
        idx_b = Tiles.index(b)

        neighbors1 = list(self.G.neighbors(b.nodes[4]))
        neighbors2 = list(self.G.neighbors(b.nodes[5]))
        
        self.G.remove_node(b.nodes[4])
        self.G.remove_node(b.nodes[5])
        
        tmp1 = b.nodes[4]
        tmp2 = b.nodes[5]

        b.nodes[4] = a.nodes[2]
        self.nodemap[(idx_b, 4)] = a.nodes[2]
        for tile in Tiles:
            for i in range(len(tile.nodes)):
                if tile.nodes[i] is tmp1:
                    tile.nodes[i] = a.nodes[2]
                    tmp_idx = Tiles.index(tile)
                    self.nodemap[(tmp_idx, i)] = a.nodes[2]

        for neighbor in neighbors1:
            if neighbor in self.G:
                self.G.add_edge(b.nodes[4], neighbor, owner = None, roadowner = None)
        
        b.nodes[5] = a.nodes[1]
        self.nodemap[(idx_b, 5)] = a.nodes[1]
        for tile in Tiles:
            for i in range(len(tile.nodes)):
                if tile.nodes[i] is tmp2:
                    tile.nodes[i] = a.nodes[1]
                    tmp_idx = Tiles.index(tile)
                    self.nodemap[(tmp_idx, i)] = a.nodes[1]

        for neighbor in neighbors2:
            if neighbor in self.G:
                self.G.add_edge(b.nodes[5], neighbor, owner = None, roadowner = None)

        #b.nodes[4].resources = list(set(b.nodes[4].resources + tmp1.resources))
        b.nodes[4].resources[0] = b.resource
        b.nodes[4].resources[2] = a.resource
        #b.nodes[4].numbers = list(set(b.nodes[4].numbers + tmp1.numbers))
        b.nodes[4].numbers[0] = b.number
        b.nodes[4].numbers[2] = a.number

        #b.nodes[5].resources = list(set(b.nodes[5].resources + tmp2.resources))
        b.nodes[5].resources[0] = b.resource
        b.nodes[5].resources[2] = a.resource
        #b.nodes[5].numbers = list(set(b.nodes[5].numbers + tmp2.numbers))
        b.nodes[5].numbers[0] = b.number
        b.nodes[5].numbers[2] = a.number
        return

board = dummyboard()
for tile in board.tiles:
    print(tile.resource)
    print(tile.number)
print(board.nodemap[(0,0)].numbers)
print(board.nodemap[(0,0)].resources)


# # Generating a list of Tiles with the resources, numbers and the 6 nodes. 
# tiles = []
# for i in range(2):
#     tiles.append(Tile(resource=resources.pop(), number = numbers.pop(), G = G))
# #     # Make a map that points to a node based off the unique id of a node. 
# for i in range(len(tiles)):
#     for j in range(len(tiles[i].nodes)):
#         if (i, j) not in nodemap:
#             nodemap[(i,j)] = tiles[i].nodes[j]


# print(len(G.nodes()))
# join0(tiles[0], tiles[1], tiles)
# print(len(G.nodes()))
# unique_nodes = set(nodemap.values())
# assert all(node in G for node in unique_nodes)


# Code for connecting the first 5 nodes

# self.join0(self.tiles[0], self.tiles[1], self.tiles)
# self.join60(self.tiles[3], self.tiles[0], self.tiles)
# self.join120(self.tiles[4], self.tiles[0], self.tiles)
# self.join0(self.tiles[1], self.tiles[2], self.tiles)
# self.join60(self.tiles[4], self.tiles[2], self.tiles)
# self.join120(self.tiles[5], self.tiles[1], self.tiles)
# self.join0(self.tiles[1], self.tiles[2], self.tiles)
# self.join60(self.tiles[5], self.tiles[2], self.tiles)
# self.join120(self.tiles[6], self.tiles[2], self.tiles)
# self.join0(self.tiles[3], self.tiles[4], self.tiles)
# self.join60(self.tiles[3], self.tiles[0], self.tiles)
# self.join60(self.tiles[7], self.tiles[3], self.tiles)
# self.join120(self.tiles[8], self.tiles[3], self.tiles)
# self.join0(self.tiles[4], self.tiles[5], self.tiles)
# self.join60(self.tiles[4], self.tiles[1], self.tiles)
# self.join120(self.tiles[4], self.tiles[0], self.tiles)
# self.join0(self.tiles[3], self.tiles[4], self.tiles)
# self.join60(self.tiles[8], self.tiles[4], self.tiles)
# self.join120(self.tiles[9], self.tiles[4], self.tiles)




