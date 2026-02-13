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
        self.resources = ["rock"] * 3 + ["mud"] * 3 + ["wheat"] * 4 + ["tree"] * 4 + ["sheep"] * 4
        self.numbers = [2,12] + 2 * [3,4,5,6,8,9,10,11]
        random.shuffle(self.resources)
        random.shuffle(self.numbers)
        interval = random.randint(0, 19)
        self.resources = self.resources[0:interval] + ['desert'] + self.resources[interval:]
        self.numbers = self.numbers[0:interval] + [-1] + self.numbers[interval:]
        self.tiles = []
        for i in range(19):
            number = self.numbers.pop()
            tmp_tile = Tile(resource=self.resources.pop(), number = number, G = self.G)
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

        return



    def getTiles(self): return self.tiles

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



    def draw_tiles_only(self):
        NODE_ANGLES = [math.radians(a) for a in [30, 330, 270, 210, 150, 90]]
        NODE_RADIUS = 1.0
        HEX_WIDTH = 2.0
        HEX_HEIGHT = math.sqrt(3)

        # Tile layout
        TILE_LAYOUT = [
            [0, 1, 2],
            [3, 4, 5, 6],
            [7, 8, 9, 10, 11],
            [12, 13, 14, 15],
            [16, 17, 18]
        ]
        
        # Compute tile centers
        tile_centers = {}
        for row_idx, row in enumerate(TILE_LAYOUT):
            x_offset = -(len(row) - 1) * HEX_WIDTH / 2.0
            y = -row_idx * HEX_HEIGHT * 0.75
            for col_idx, tile_idx in enumerate(row):
                tile_centers[tile_idx] = (x_offset + col_idx * HEX_WIDTH, y)

        # Compute the 6 corner positions for each tile
        def get_corners(tile_idx):
            cx, cy = tile_centers[tile_idx]
            return [(cx + NODE_RADIUS * math.cos(NODE_ANGLES[i]),
                    cy + NODE_RADIUS * math.sin(NODE_ANGLES[i])) for i in range(6)]

        # Build a unique node registry based on rounded coordinates
        node_registry = {}  # (rounded_x, rounded_y) -> unique_node_id
        next_node_id = 0
        tile_nodes = {}  # tile_idx -> [6 unique node IDs]
        
        for tile_idx in range(19):
            corners = get_corners(tile_idx)
            tile_nodes[tile_idx] = []
            
            for corner in corners:
                # Round to avoid floating point issues
                key = (round(corner[0], 6), round(corner[1], 6))
                
                if key not in node_registry:
                    node_registry[key] = next_node_id
                    next_node_id += 1
                
                tile_nodes[tile_idx].append(node_registry[key])

        # Create a reverse mapping for plotting
        node_positions = {node_id: key for key, node_id in node_registry.items()}

        # Draw
        fig, ax = plt.subplots(figsize=(14, 12))
        ax.set_aspect('equal')

        # Polygon winding order
        WINDING = [0, 5, 4, 3, 2, 1]

        for tile_idx in range(19):
            corners = get_corners(tile_idx)
            poly_corners = [corners[i] for i in WINDING]

            # Draw hex
            polygon = plt.Polygon(poly_corners, facecolor='#DDDDDD', edgecolor='#555555', linewidth=1.5, zorder=1)
            ax.add_patch(polygon)

            # Tile index label at center
            cx, cy = tile_centers[tile_idx]
            ax.text(cx, cy, str(tile_idx), ha='center', va='center',
                    fontsize=14, fontweight='bold', color='#333333', zorder=2)

        # Draw unique nodes (only once each)
        for node_id, (nx, ny) in node_positions.items():
            ax.plot(nx, ny, 'o', color='#42A5F5', markersize=8,
                    markeredgecolor='black', markeredgewidth=1.5, zorder=3)
            
            # Find center of nearest tile for offset direction
            min_dist = float('inf')
            nearest_center = None
            for tile_idx in range(19):
                cx, cy = tile_centers[tile_idx]
                dist = math.sqrt((nx - cx)**2 + (ny - cy)**2)
                if dist < min_dist:
                    min_dist = dist
                    nearest_center = (cx, cy)
            
            cx, cy = nearest_center
            dx = nx - cx
            dy = ny - cy
            length = math.sqrt(dx*dx + dy*dy)
            ox = nx + (dx / length) * 0.25
            oy = ny + (dy / length) * 0.25
            
            ax.text(ox, oy, str(node_id), ha='center', va='center',
                    fontsize=7, color='red', zorder=4)

        ax.set_title(f"Tiles with unique nodes (Total: {next_node_id} nodes)", fontsize=16, fontweight='bold')
        ax.axis('off')
        plt.tight_layout()
        plt.show()
    # tilemaplist = [{0:1, 240: 3, 300: 4},
    #         {0: 2, 180: 0, 240: 4, 300: 5},
    #         {180: 1, 240: 5, 300: 6},
    #         {0:4, 60: 0, 240: 7, 300: 8},
    #         {0:5, 60:1, 120:0, 180:3, 240: 8, 300: 9},
    #         {0:6, 60: 2, 120: 1, 180: 4, 240: 9, 300: 10},
    #         {120:2, 180:5, 240:10, 300:11},
    #         {0:8, 60:3,300:12},
    #         {0:9, 60:4, 120:3, 180:7, 240:12,300:13},
    #         {0:10, 60:5, 120:4, 180:8, 240:13, 300:14},
    #         {0:11, 60:6, 120:5, 180:9, 240:14, 300:15},
    #         {120:6, 180: 10, 240:15},
    #         {0:13, 60:8,120:7,300:16},
    #         {0:14, 60:9, 120:8,180:12,240:16, 300:17},
    #         {0:15, 60:10, 120:9, 180:13, 240:17, 300:18},
    #         {60:11, 120:10, 180:14, 240:18},
    #         {0:17, 60:13, 120:12},
    #         {0:18, 60:14, 120:13, 180:16},
    #         {60:15, 120:14, 180:17}]


# board = Board()
# G = board.G
    # Debugger Function
