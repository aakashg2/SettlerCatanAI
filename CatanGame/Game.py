from CatanGame.Player import Player
from CatanGame.Board import Board
import random
import ast
class Game:
    players = []
    VP_to_win = 10
    discard_limit = 7
    current_turn = None # Tells us whose turn it is
    board = None
    turn_number = 0 # Keeps track of the total number of turns
    longest_road = None
    largest_army = None
    
    def __init__(self, num_players: int, board: Board, VP_to_win: int, discard_limit: int, debug = False):
        self.board = board
        self.VP_to_win = VP_to_win
        self.discard_limit = discard_limit
        if debug:
            default_players = [
            ("Pesto", "Green"),
            ("Sky", "Blue"),
            ("Grape", "Green"),
            ("Banana", "Yellow")
            ]
            for i in range(num_players):
                name, color = default_players[i]
                self.players.append(Player(name, color))
        else:
            for i in range(num_players):
                print("Player " + str(i+1) + ": Please enter your name and color as (name, color)") 
                raw = input()
                name, color = raw.split(",")
                name = name.strip()
                color = color.strip()
                self.players.append(Player(name, color))
        self.displayPlayers()
        print("We will now randomize order")
        random.shuffle(self.players)
        return
    def displayPlayers(self):
        for player in self.players:
            print("---")
            print(player.display_player_info())
            print("---")
    

    
    def setupPhase(self, debug = False):
        assert self.board != None
        if debug:
            # Predefined starting positions for quick testing
            # Format: {player_index: [(settlement1, road1), (settlement2, road2)]}
            debug_positions = {
                0: [  # Player 1
                    ((0, 0), ((0, 0), (0, 1))),  # settlement1, road1
                    ((2, 1), ((2, 1), (2, 2)))   # settlement2, road2
                ],
                1: [  # Player 2
                    ((3, 0), ((3, 0), (3, 1))),
                    ((7, 5), ((7, 5), (7, 4)))
                ],
                2: [  # Player 3
                    ((5, 4), ((9, 0), (9, 1))),
                    ((10, 4), ((10, 4), (10, 3)))
                ],
                3: [  # Player 4
                    ((18, 0), ((18, 0), (18, 1))),
                    ((16, 0), ((16, 0), (17, 1)))
                ]
            }
            
            # First round
            for idx, player in enumerate(self.players):
                if idx < len(debug_positions):
                    settlement, road = debug_positions[idx][0]
                    tile_idx, node_idx = settlement
                    road_starting, road_ending = road
                    
                    player.build_settlement(self.board, tile_idx, node_idx, setup=True)
                    player.build_road(self.board, road_starting, road_ending, setup=True)
                    print(f"DEBUG: {player.name} placed settlement at {settlement} and road from {road_starting} to {road_ending}")
            
            # Second round (reverse order)
            for idx, player in enumerate(self.players[::-1]):
                player_idx = len(self.players) - 1 - idx
                if player_idx < len(debug_positions):
                    settlement, road = debug_positions[player_idx][1]
                    tile_idx, node_idx = settlement
                    road_starting, road_ending = road
                    
                    player.build_settlement(self.board, tile_idx, node_idx, setup=True)
                    player.build_road(self.board, road_starting, road_ending, setup=True)
                    print(f"DEBUG: {player.name} placed settlement at {settlement} and road from {road_starting} to {road_ending}")
        else:
            for player in self.players:
                while True:
                    raw = input("Player " + str(player.name) + ", please input your starting settlement as (Tile_idx, Node_idx): ")
                    tile_idx, node_idx = ast.literal_eval(raw)
                    if player.build_settlement(self.board, tile_idx, node_idx, setup = True) == "Created a Settlement":
                        break
                    print("Place a valid spot")
                while True:
                    raw = input("Player " + str(player.name) + ", please input your starting road as (Tile_idx, Node_idx) and ending road as (Tile_idx, Node_idx)")
                    road_starting, road_ending = ast.literal_eval(raw)
                    if player.build_road(self.board, road_starting, road_ending, setup = True) == "Added the Road":
                        break
                    print("Place a valid spot")

            for player in self.players[::-1]:
                while True:
                    raw = input("Player " + str(player.name) + ", please input your starting settlement as (Tile_idx, Node_idx): ")
                    tile_idx, node_idx = ast.literal_eval(raw)
                    if player.build_settlement(self.board, tile_idx, node_idx, setup = True) == "Created a Settlement":
                        break
                    print("Place a valid spot")
                while True:
                    raw = input("Player " + str(player.name) + ", please input your starting road as (Tile_idx, Node_idx) and ending road as (Tile_idx, Node_idx)")
                    road_starting, road_ending = ast.literal_eval(raw)
                    if player.build_road(self.board, road_starting, road_ending, setup = True) == "Added the Road":
                        break
                    print("Place a valid spot")
            
            self.displayPlayers()
        return
    def rollDice(self, player: Player):
        roll = random.randint(1,6) + random.randint(1,6)
        print("A " + str(roll) + " has been rolled")
        if roll == 7:
            
            location = int(input("Which Tile do you want to place this robber on?"))
            assert type(location) is int
            susceptible_players = None
            tile = self.board.tiles[location]
            for node in tile.nodes:
                if node.owner != None:
                    susceptible_players = [player for player in self.players if ((node.owner == player.name) and (sum(player.cards.values()) != 0))]
            if (susceptible_players == []):
                print("No Cards to Take")
                return
            print('Which player would you want to take from?')
            print(susceptible_players)            
            index = int(input("Enter the idx"))
            assert type(index) is int
            player_to_steal = susceptible_players[index]
            card = player_to_steal.removeCards()
            player.addCards(1, card)
            print("Player " + str(player.name) +" has stolen " + str(card) + " from " + str(player_to_steal.name))
            return
            

        # Get a list of player owned settlements
        for player in self.players:
            harvested_resources = []
            for val in player.rollmap[roll]:
                num_cards, resource = val
                player.addCards(num_cards, resource)
                harvested_resources.append([resource] * num_cards)
            print("Player " + str(player.name) + " has recieved " + str(harvested_resources))
        return
    def StartTradingPhase(self, player: Player):
        # Display Player 1 cards

        # Ask if it wants to trade

        # Ask it what cards to trade Want -> Receive

        # Go by By turn ask each each player if it wants to accept, reject, or get a counteroffer

        # List the other players responses and allow player 1 decide what he wants to do (accept or reject player i's offer)

        # Ask if it would like to trade again

        # End if it says no

        return
    def StartBuildingPhase(self, player: Player):
        # Ask if player 1 wants to build a road

        # Ask if player 1 wants to build a settlement

        # Ask if player 1 wants to build a city

        # Ask if player 1 wants to buy a dev card
        return
    def ControlRobber(self, player: Player):
        return
    
