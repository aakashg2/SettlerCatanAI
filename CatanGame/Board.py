import networkx as nx
import math
import string
import matplotlib.pyplot as plt
import scipy
import random
from .Tile import Tile


class Board:
    G = nx.Graph()
    nodemap = {}
    resources = None
    numbers = None
    tiles = []
    robber = None
    devCards = []
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
    die = {}
    for i in range(2,13):
        die[i] = []
    die[-1] = []
    
    def __init__(self):
        self.G = nx.Graph()
        self.nodemap = {}
        self.resources = ["rock"] * 3 + ["mud"] * 3 + ["wheat"] * 4 + ["wood"] * 4 + ["sheep"] * 4
        self.numbers = [2,12] + 2 * [3,4,5,6,8,9,10,11]
        self.devCards = ['Knight'] * 14 + ['Road Building'] * 2 + ['YOP'] * 2 + ['Mono'] * 2 + ['VP'] * 5
        random.shuffle(self.devCards)
        random.shuffle(self.resources)
        random.shuffle(self.numbers)
        interval = random.randint(0, 19)
        self.robber = interval
        self.resources = self.resources[0:interval] + ['desert'] + self.resources[interval:]
        self.numbers = self.numbers[0:interval] + [-1] + self.numbers[interval:]
        self.tiles = []
        for i in range(19):
            number = self.numbers.pop()
            resource = self.resources.pop()
            tmp_tile = Tile(resource=resource, number = number, G = self.G)
            self.tiles.append(tmp_tile)
            self.die[number].append(tmp_tile)

        
        for i in range(len(self.tiles)):
            for j in range(len(self.tiles[i].nodes)):
                if (i, j) not in self.nodemap:
                    self.nodemap[(i,j)] = self.tiles[i].nodes[j]

        for i, tilemap in enumerate(self.tilemaplist):
            for direction in list(tilemap.keys()):
                if direction == 0:
                    self.join0(self.tiles[i], self.tiles[tilemap[direction]], self.tiles)
                elif direction == 60:
                    self.join60(self.tiles[i], self.tiles[tilemap[direction]], self.tiles)
                elif direction == 120:
                    self.join120(self.tiles[i], self.tiles[tilemap[direction]], self.tiles)
                elif direction == 180:
                    self.join0(self.tiles[tilemap[direction]], self.tiles[i], self.tiles)
                elif direction == 240:
                    self.join60(self.tiles[tilemap[direction]], self.tiles[i], self.tiles)
                else:
                    self.join120(self.tiles[tilemap[direction]], self.tiles[i], self.tiles)
        
        seen = set()
        for (tile_idx, node_idx), node in sorted(self.nodemap.items()):
            if id(node) in seen:
                continue
            seen.add(id(node))
            if node.resources == [None] * 3:
                node.resources = [self.tiles[tile_idx].resource, None, None]

        return



    def getTiles(self): return self.tiles

    def debug_nodes(self):
        """Print every unique node with its (tile_idx, node_idx) keys, resources, numbers, and owner."""
        W_ALIAS = 50
        W_RES   = 36
        W_NUM   = 28
        W_OWNER = 12
        header = (
            "aliases (tile_idx,node_idx)[tile_resource]".center(W_ALIAS) + " | " +
            "node resources".center(W_RES) + " | " +
            "numbers".center(W_NUM) + " | " +
            "owner".center(W_OWNER)
        )
        print(header)
        print("-" * len(header))

        seen = set()
        for (tile_idx, node_idx), node in sorted(self.nodemap.items()):
            if id(node) in seen:
                continue
            seen.add(id(node))
            aliases_str    = "  ".join(
                f"({t},{n})[{self.tiles[t].resource}]"
                for (t, n), nd in sorted(self.nodemap.items()) if nd is node
            )
            resources_str  = str(node.resources)
            numbers_str    = str(node.numbers)
            owner_str      = str(node.owner)
            print(
                aliases_str.center(W_ALIAS) + " | " +
                resources_str.center(W_RES) + " | " +
                numbers_str.center(W_NUM) + " | " +
                owner_str.center(W_OWNER)
            )


    # When Tile A is to the left of Tile B
    def join0(self,  a: Tile, b: Tile, Tiles):
        idx_a = Tiles.index(a)
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
        b.nodes[2].resources_idx[2] = idx_b
        b.nodes[2].resources_idx[1] = idx_a
        #b.nodes[2].numbers = list(set(b.nodes[2].numbers + tmp1.numbers))
        b.nodes[2].numbers[2] = b.number
        b.nodes[2].numbers[1] = a.number
        
        #b.nodes[3].resources = list(set(b.nodes[3].resources + tmp2.resources))
        b.nodes[3].resources[0] = a.resource
        b.nodes[3].resources[1] = b.resource
        b.nodes[2].resources_idx[0] = idx_a
        b.nodes[3].resources_idx[1] = idx_b
        #b.nodes[3].numbers = list(set(b.nodes[3].numbers + tmp2.numbers))
        b.nodes[3].numbers[0] = a.number
        b.nodes[3].numbers[1] = b.number

        return

    def join60(self, a: Tile, b: Tile, Tiles):
        idx_b = Tiles.index(b)
        idx_a = Tiles.index(a)
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
        a.nodes[1].resources_idx[1] = idx_b
        a.nodes[1].resources_idx[2] = idx_a
        #a.nodes[1].numbers = list(set(a.nodes[1].numbers + tmp1.numbers))  
        a.nodes[1].numbers[1] = b.number
        a.nodes[1].numbers[2] = a.number

        #a.nodes[0].resources = list(set(a.nodes[0].resources + tmp2.resources))
        a.nodes[0].resources[0] = b.resource
        a.nodes[0].resources[1] = a.resource
        a.nodes[0].resources_idx[0] = idx_b
        a.nodes[0].resources_idx[1] = idx_a
        #a.nodes[0].numbers = list(set(a.nodes[0].numbers + tmp2.numbers))
        a.nodes[0].numbers[0] = b.number
        a.nodes[0].numbers[1] = a.number
        return

    def join120(self, a: Tile, b: Tile, Tiles):
        idx_b = Tiles.index(b)
        idx_a = Tiles.index(a)
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
        b.nodes[4].resources_idx[0] = idx_b
        b.nodes[4].resources_idx[2] = idx_a
        #b.nodes[4].numbers = list(set(b.nodes[4].numbers + tmp1.numbers))
        b.nodes[4].numbers[0] = b.number
        b.nodes[4].numbers[2] = a.number

        #b.nodes[5].resources = list(set(b.nodes[5].resources + tmp2.resources))
        b.nodes[5].resources[0] = b.resource
        b.nodes[5].resources[2] = a.resource
        b.nodes[5].resources_idx[0] = idx_b
        b.nodes[5].resources_idx[2] = idx_a
        #b.nodes[5].numbers = list(set(b.nodes[5].numbers + tmp2.numbers))
        b.nodes[5].numbers[0] = b.number
        b.nodes[5].numbers[2] = a.number
        return



