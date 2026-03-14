from .Board import Board
from .Node import Node
import random
class Player:
    name = None
    color = None
    cards = None
    num_VPs = 0
    roads_inventory = 15
    settlements = []
    cities = []
    rollmap = None
    settlements_inventory = 5
    cities_inventory = 4
    dev_cards_inventory = None
    has_longest_road = False
    has_largest_army = False
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.cards = {"rock": 0, "wood": 0, "wheat": 0, "mud": 0, "sheep": 0}
        self.num_VPs = 0
        self.roads_inventory = 15
        self.settlements = []
        self.cities = []
        self.settlements_inventory = 5
        self.cities_inventory = 4
        self.dev_cards_inventory = []
        self.has_longest_road = False
        self.has_largest_army = False
        self.rollmap = {}
        for i in range(2,13):
            self.rollmap[i] = []
            self.rollmap[-1] = []
    
    def display_player_info(self):
        print(f"Player Name: {self.name}")
        print(f"Player Color: {self.color}")
        print(f"Number of Cards: {sum(self.cards.values())}")
        print(f"Number of Victory Points: {self.num_VPs}")
        print(f"Roads Inventory: {self.roads_inventory}")
        print(f"Settlements Inventory: {self.settlements_inventory}")
        print(f"Cities Inventory: {self.cities_inventory}")
        print(f"Development Cards Inventory: {self.dev_cards_inventory}")
        print(f"Has Longest Road: {self.has_longest_road}")
        print(f"Has Largest Army: {self.has_largest_army}")
        return
    
    def build_settlement(self, board: Board, tile_idx, node_idx, setup = False):
        # Check if there are any settlements around or if Node is occupied
        node = board.nodemap[(tile_idx, node_idx)]
        neighbors = board.G.neighbors(node)
        if ((node.owner != None) or any(node.owner != None for node in neighbors)): return "Invalid Spot"
        if self.settlements_inventory == 0:
            return "Cant place anymore settlements"
        # Check if you have the appropriate resources
        if setup: # Setup Mode doesnt require resources
            self.settlements.append((tile_idx, node_idx))
            node.owner = self.name
            self.settlements_inventory-=1
            self.num_VPs+=1
            for i in range(len(node.numbers)):
                if node.numbers[i] != None:
                    self.rollmap[node.numbers[i]].append((1, node.resources[i], node.resources_idx[i]))
            return "Created a Settlement"
        if ((self.cards['mud'] >= 1) and (self.cards['sheep'] >= 1) and (self.cards['wood'] >= 1) and (self.cards['wheat'] >= 1)):
            self.cards['mud'] -=1
            self.cards['sheep'] -= 1
            self.cards['wood'] -=1
            self.cards['wheat'] -=1
            self.settlements.append((tile_idx, node_idx))
            node.owner = self.name
            self.settlements_inventory-=1
            self.num_VPs+=1
            for i in range(len(node.numbers)):
                if node.numbers[i] != None:
                    self.rollmap[node.numbers[i]].append((1, node.resources[i], node.resources_idx[i]))
            return "Created a Settlement"
        else:
            return "You dont have the required resources"
    
    def build_city(self, Board, tile_idx, node_idx):
        # Check if you have enough cities left
        if (self.cities_inventory == 0):
            return "Not enough cities"
        if (self.settlements_inventory == 5):
           return "You need to build a settlement first!" 
        if not ((self.cards['rock'] >= 3) or (self.cards['wheat'] >= 2)):
            self.cards['rock'] -= 3
            self.cards['wheat'] -= 2
            self.cities_inventory -=1
            self.settlements_inventory+=1
            self.cities.append((tile_idx, node_idx))
            self.settlements.remove((tile_idx, node_idx))
            self.num_VPs+=1
            node = Board.nodemap[(tile_idx, node_idx)]
            for i in range(len(node.numbers)):
                self.rollmap[(node.numbers[i])] = [(x+1, y, z) for x,y,z in self.rollmap[(node.numbers[i])]]
            return "Created a city"
        else:
            return "Insufficient Cards"
    
    def build_road(self, Board: Board, startingposition: tuple, endingposition: tuple, setup = False):
        if not ((self.cards['wood'] >= 1 and self.cards['mud'] >= 1) or (setup)):
            return "You dont have the required resources"
        beginningnode = Board.nodemap[(startingposition)]
        endingnode = Board.nodemap[(endingposition)]
        assert ((beginningnode in Board.G) and (endingnode in Board.G))
        if (beginningnode.owner == self.name): # Check if road is connected to the player's settle
            if (Board.G[beginningnode][endingnode]['roadowner'] == None): # Ensure the edge is unoccupied
                Board.G[beginningnode][endingnode]['roadowner'] = self.name
                self.roads_inventory-=1
                if not setup: 
                    self.cards['wood']-=1
                    self.cards['mud']-=1
                return "Added the Road"
            else:
                return "Your road or someone else's road is in the way"
        else: # Road is not connected to the players settle
            neighbors = Board.G.neighbors(beginningnode)
            neighbor_edges = []
            total_neighbor_edges = []
            for neighbor in neighbors:
                total_neighbor_edges.append(Board.G[beginningnode][neighbor]['roadowner'])
                if Board.G[beginningnode][neighbor]['roadowner'] != self.name:
                    neighbor_edges.append(Board.G[beginningnode][neighbor]['roadowner'])
            
            if (beginningnode.owner != self.name and beginningnode.owner != None): # Foreign settlement checker
                return "Foreign Settlement is in the way"
                
            elif any(edge == self.name for edge in total_neighbor_edges): # Check if your road is connected to your own road
                if Board.G[beginningnode][endingnode]['roadowner'] == None:
                    Board.G[beginningnode][endingnode]['roadowner'] = self.name
                    self.roads_inventory-=1
                    if not setup:
                        self.cards['wood']-=1
                        self.cards['mud']-=1
                    return "Added the Road"
                else:
                    return "Another road is in the way"
            else:
                return "Your road must connect to a road that you own"

    def removeCards(self): # Function used to remove a random card when robbing a player
        num_cards = sum(self.cards.values())
        if num_cards == 0:
            return None
        random_idx = random.randint(0, num_cards-1)
        for key in self.cards.keys():
            if self.cards[key] > 0:
                if (random_idx - self.cards[key]) < 0:
                    self.cards[key]-=1
                    return key
                else:
                    random_idx-=self.cards[key]
        return "You shouldnt be here"

    def addCards(self, num_resources, ResourceType):
        if ResourceType == None or ResourceType == 'desert': return "Resource is None or desert"
        if ResourceType.lower() in self.cards:
            self.cards[ResourceType.lower()]+=num_resources
        else:
            print("That does not match a resource")
        return
        # Get a list of settlements