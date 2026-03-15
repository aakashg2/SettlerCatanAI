from CatanGame.Player import Player
from CatanGame.Board import Board
import random
import ast
import networkx as nx
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
            ("Grape", "White"),
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
        #random.shuffle(self.players)
        return
    def displayPlayers(self):
        for player in self.players:
            print("---")
            print(player.display_player_info())
            print("---")

    def _valid_node(self, tile_idx, node_idx):
        """Return True if (tile_idx, node_idx) is a valid key in the board nodemap."""
        return (
            isinstance(tile_idx, int) and isinstance(node_idx, int) and
            0 <= tile_idx <= 18 and 0 <= node_idx <= 5 and
            (tile_idx, node_idx) in self.board.nodemap
        )

    def _valid_road(self, start, end):
        """Return True if both road endpoints are valid nodemap keys."""
        return (
            isinstance(start, tuple) and isinstance(end, tuple) and
            len(start) == 2 and len(end) == 2 and
            self._valid_node(start[0], start[1]) and
            self._valid_node(end[0], end[1]) and 
            self.board.G.has_edge(self.board.nodemap[start], self.board.nodemap[end])
        )
    def _valid_settle(self, tile_idx, node_idx, player):
        node = self.board.nodemap[(tile_idx, node_idx)]
        for u,v in self.board.G.edges(node):
            if self.board.G[u][v]['roadowner'] == player.name:
                return True
        return False

    def _check_winner(self):
        for player in self.players:
            if player.num_VPs >= self.VP_to_win:
                print("Player " + str(player.name) + " has won the game with " + str(player.num_VPs))
                return True
        return False
    
    def setupPhase(self, debug=False, on_update=None):
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
                    if on_update: on_update()
                    player.build_road(self.board, road_starting, road_ending, setup=True)
                    if on_update: on_update()
                    print(f"DEBUG: {player.name} placed settlement at {settlement} and road from {road_starting} to {road_ending}")

            # Second round (reverse order)
            for idx, player in enumerate(self.players[::-1]):
                player_idx = len(self.players) - 1 - idx
                if player_idx < len(debug_positions):
                    settlement, road = debug_positions[player_idx][1]
                    tile_idx, node_idx = settlement
                    road_starting, road_ending = road

                    player.build_settlement(self.board, tile_idx, node_idx, setup=True)
                    node = self.board.tiles[tile_idx].nodes[node_idx]
                    if on_update: on_update()
                    player.build_road(self.board, road_starting, road_ending, setup=True)
                    if on_update: on_update()
                    print(f"DEBUG: {player.name} placed settlement at {settlement} and road from {road_starting} to {road_ending}")
                    print('Player ' + str(player.name) + " got starting resources " + str(node.resources))
                    for resource in node.resources:
                        player.addCards(1, resource)
        else:
            for player in self.players:
                while True:
                    try:
                        tile_idx, node_idx = ast.literal_eval(input("Player " + str(player.name) + ", please input your starting settlement as (Tile_idx, Node_idx): "))
                    except (ValueError, SyntaxError, TypeError):
                        print("Invalid format. Use (tile_idx, node_idx).")
                        continue
                    if not self._valid_node(tile_idx, node_idx):
                        print(f"Out of bounds: tile_idx must be 0-18, node_idx must be 0-5.")
                        continue
                    if player.build_settlement(self.board, tile_idx, node_idx, setup=True) == "Created a Settlement":
                        if on_update: on_update()
                        break
                    print("Place a valid spot")
                while True:
                    try:
                        road_starting, road_ending = ast.literal_eval(input("Player " + str(player.name) + ", please input your starting road as (Tile_idx, Node_idx) and ending road as (Tile_idx, Node_idx): "))
                    except (ValueError, SyntaxError, TypeError):
                        print("Invalid format. Use ((tile_idx, node_idx), (tile_idx, node_idx)).")
                        continue
                    if not self._valid_road(road_starting, road_ending):
                        print(f"Out of bounds: tile_idx must be 0-18, node_idx must be 0-5.")
                        continue
                    if player.build_road(self.board, road_starting, road_ending, setup=True) == "Added the Road":
                        if on_update: on_update()
                        break
                    print("Place a valid spot")

            for player in self.players[::-1]:
                while True:
                    try:
                        tile_idx, node_idx = ast.literal_eval(input("Player " + str(player.name) + ", please input your starting settlement as (Tile_idx, Node_idx): "))
                    except (ValueError, SyntaxError, TypeError):
                        print("Invalid format. Use (tile_idx, node_idx).")
                        continue
                    if not self._valid_node(tile_idx, node_idx):
                        print(f"Out of bounds: tile_idx must be 0-18, node_idx must be 0-5.")
                        continue
                    if player.build_settlement(self.board, tile_idx, node_idx, setup=True) == "Created a Settlement":
                        node = self.board.tiles[tile_idx].nodes[node_idx]
                        for resource in node.resources:
                            player.addCards(1, resource)
                        if on_update: on_update()
                        break
                    print("Place a valid spot")
                while True:
                    try:
                        road_starting, road_ending = ast.literal_eval(input("Player " + str(player.name) + ", please input your starting road as (Tile_idx, Node_idx) and ending road as (Tile_idx, Node_idx): "))
                    except (ValueError, SyntaxError, TypeError):
                        print("Invalid format. Use ((tile_idx, node_idx), (tile_idx, node_idx)).")
                        continue
                    if not self._valid_road(road_starting, road_ending):
                        print(f"Out of bounds: tile_idx must be 0-18, node_idx must be 0-5.")
                        continue
                    if player.build_road(self.board, road_starting, road_ending, setup=True) == "Added the Road":
                        if on_update: on_update()
                        break
                    print("Place a valid spot")

            self.displayPlayers()
        return
    
    def _discard_phase(self):
        import math
        for player in self.players:
            total = sum(player.cards.values())
            if total > self.discard_limit:
                to_discard = math.floor(total / 2)
                print(f"\n{player.name} has {total} cards (limit {self.discard_limit}) and must discard {to_discard}.")
                discarded = 0
                while discarded < to_discard:
                    remaining = to_discard - discarded
                    print(f"  Cards: {player.cards}  |  Still need to discard: {remaining}")
                    resource = input(f"  {player.name}, choose a resource to discard: ").strip().lower()
                    if resource not in player.cards:
                        print(f"  Invalid resource. Choose from: {list(player.cards.keys())}")
                        continue
                    if player.cards[resource] == 0:
                        print(f"  You have no {resource} to discard.")
                        continue
                    try:
                        amount = int(input(f"  How many {resource} to discard (you have {player.cards[resource]}, need to discard {remaining} more)? "))
                    except ValueError:
                        print("  Enter a valid number.")
                        continue
                    if amount <= 0:
                        print("  Must discard at least 1.")
                        continue
                    if amount > player.cards[resource]:
                        print(f"  You only have {player.cards[resource]} {resource}.")
                        continue
                    if amount > remaining:
                        print(f"  You only need to discard {remaining} more.")
                        continue
                    player.cards[resource] -= amount
                    discarded += amount
                print(f"  {player.name} discarded {to_discard} cards. Remaining: {player.cards}")

    def rollDice(self, player: Player):
        roll = random.randint(1,6) + random.randint(1,6)
        print("A " + str(roll) + " has been rolled")
        if roll == 7:
            self._discard_phase()
            self.StealCard(player)
        else:
            # Get a list of player owned settlements
            for player in self.players:
                harvested_resources = []
                for val in player.rollmap[roll]:
                    num_cards, resource, tile_idx = val
                    if tile_idx != self.board.robber:
                        player.addCards(num_cards, resource)
                        harvested_resources.append([resource] * num_cards)
                    else:
                        print("Tile " + str(tile_idx) + " has been blocked by the robber")
                print("Player " + str(player.name) + " has recieved " + str(harvested_resources))
        return
    
    def StealCard(self, player1: Player):
        location = int(input("Which Tile do you want to place this robber on?"))
        assert type(location) is int
        self.board.robber = location
        susceptible_players = None
        tile = self.board.tiles[location]
        for node in tile.nodes:
            if node.owner != None:
                susceptible_players = [player for player in self.players if ((node.owner == player.name) and (sum(player.cards.values()) != 0))]
        if (susceptible_players == []):
            print("No Cards to Take")
            return
        print('Which player would you want to take from?')
        print([p.name for p in susceptible_players])            
        index = int(input("Enter the idx"))
        assert type(index) is int
        player_to_steal = susceptible_players[index]
        card = player_to_steal.removeCards()
        player1.addCards(1, card)
        print("Player " + str(player1.name) +" has stolen " + str(card) + " from " + str(player_to_steal.name))
        return

    def StartTradingPhase(self, player: Player):

        # Ask if player wants to trade
        while True:
            print(f"\n--- {player.name}'s Trading Phase ---")
            print(f"Cards: {player.cards}")
            trade_again = input("Would you like to trade? (yes/no): ").strip().lower()
            
            if trade_again == "no":
                break
            if trade_again != "yes":
                print("Please enter 'yes' or 'no'.")
                continue

            # Ask what cards to offer and what they want in return
            print("Available resources: rock, wood, wheat, mud, sheep")
            print(f"Your current cards: {player.cards}")

            offer = {}
            request = {}

            # Build offer
            print("\n--- What are you offering? ---")
            for resource in player.cards:
                while True:
                    try:
                        amount = int(input(f"How many {resource} are you offering? (you have {player.cards[resource]}): "))
                        if 0 <= amount <= player.cards[resource]:
                            if amount > 0:
                                offer[resource] = amount
                            break
                        else:
                            print(f"You only have {player.cards[resource]} {resource}.")
                    except ValueError:
                        print("Please enter a valid number.")

            if not offer:
                print("You must offer at least one resource.")
                continue

            # Build request
            print("\n--- What are you requesting in return? ---")
            all_resources = ["rock", "wood", "wheat", "mud", "sheep"]
            for resource in all_resources:
                while True:
                    try:
                        amount = int(input(f"How many {resource} do you want? "))
                        if amount >= 0:
                            if amount > 0:
                                request[resource] = amount
                            break
                        else:
                            print("Please enter a non-negative number.")
                    except ValueError:
                        print("Please enter a valid number.")

            if not request:
                print("You must request at least one resource.")
                continue

            print(f"\n{player.name} is offering {offer} in exchange for {request}")

            # Go through each other player and ask if they accept, reject, or counteroffer
            responses = {}  # player_name -> ("accept" | "reject" | "counteroffer", counteroffer_dict or None)

            other_players = [p for p in self.players if p.name != player.name]

            for other_player in other_players:
                print(f"\n--- {other_player.name}'s turn to respond ---")
                print(f"{other_player.name}'s cards: {other_player.cards}")

                while True:
                    response = input(f"{other_player.name}, do you accept, reject, or counteroffer? ").strip().lower()

                    if response == "reject":
                        responses[other_player.name] = ("reject", None)
                        print(f"{other_player.name} has rejected the offer.")
                        break

                    elif response == "accept":
                        # Check if other_player has the requested resources
                        can_fulfill = all(other_player.cards.get(r, 0) >= amt for r, amt in request.items())
                        if not can_fulfill:
                            print(f"{other_player.name} does not have enough resources to fulfill this request.")
                            responses[other_player.name] = ("reject", None)
                        else:
                            responses[other_player.name] = ("accept", None)
                            print(f"{other_player.name} has accepted the offer.")
                        break

                    elif response == "counteroffer":
                        print(f"\n{other_player.name}, enter your counteroffer:")
                        counter_offer = {}
                        counter_request = {}

                        print("What are you offering in return?")
                        for resource in all_resources:
                            while True:
                                try:
                                    amount = int(input(f"  {resource} (you have {other_player.cards.get(resource, 0)}): "))
                                    if 0 <= amount <= other_player.cards.get(resource, 0):
                                        if amount > 0:
                                            counter_offer[resource] = amount
                                        break
                                    else:
                                        print(f"You only have {other_player.cards.get(resource, 0)} {resource}.")
                                except ValueError:
                                    print("Please enter a valid number.")

                        print("What are you requesting in return?")
                        for resource in all_resources:
                            while True:
                                try:
                                    amount = int(input(f"  {resource}: "))
                                    if amount >= 0:
                                        if amount > 0:
                                            counter_request[resource] = amount
                                        break
                                    else:
                                        print("Please enter a non-negative number.")
                                except ValueError:
                                    print("Please enter a valid number.")

                        responses[other_player.name] = ("counteroffer", (counter_offer, counter_request))
                        print(f"{other_player.name} counteroffers: gives {counter_offer}, wants {counter_request}")
                        break
                    else:
                        print("Please enter 'accept', 'reject', or 'counteroffer'.")

            # List all responses and let the active player decide what to do
            print(f"\n--- {player.name}, here are the responses to your offer ---")
            accepting_players = []
            for other_player in other_players:
                status, details = responses[other_player.name]
                if status == "accept":
                    print(f"  {other_player.name}: ACCEPTED your offer")
                    accepting_players.append(other_player)
                elif status == "reject":
                    print(f"  {other_player.name}: REJECTED your offer")
                elif status == "counteroffer":
                    counter_offer, counter_request = details
                    print(f"  {other_player.name}: COUNTEROFFER — gives {counter_offer}, wants {counter_request}")

            if not accepting_players and not any(v[0] == "counteroffer" for v in responses.values()):
                print("No players accepted or made a counteroffer. Trade cancelled.")
                continue

            # Let player 1 choose who to trade with (accepts first, then counteroffers)
            tradeable_players = {}
            for other_player in other_players:
                status, details = responses[other_player.name]
                if status in ("accept", "counteroffer"):
                    tradeable_players[other_player.name] = (status, details, other_player)

            if not tradeable_players:
                print("No trade partners available.")
                continue

            print(f"\n{player.name}, who would you like to trade with? (or type 'none' to cancel)")
            for name in tradeable_players:
                print(f"  {name}")

            chosen = input("Enter player name: ").strip()
            if chosen.lower() == "none" or chosen not in tradeable_players:
                print("Trade cancelled.")
                continue

            status, details, chosen_player = tradeable_players[chosen]

            # Finalize the trade — handle accept or counteroffer
            if status == "accept":
                final_offer = offer
                final_request = request
            else:  # counteroffer — player must decide to accept or reject
                counter_offer, counter_request = details
                print(f"\n{chosen_player.name}'s counteroffer: they give {counter_offer}, they want {counter_request}")
                decision = input(f"{player.name}, do you accept this counteroffer? (yes/no): ").strip().lower()
                if decision != "yes":
                    print("Counteroffer rejected. Trade cancelled.")
                    continue
                # Flip perspective: what chosen_player offers is what player receives, and vice versa
                final_offer = counter_request   # what player must give
                final_request = counter_offer   # what player receives

                # Validate player has enough for the counteroffer
                if not all(player.cards.get(r, 0) >= amt for r, amt in final_offer.items()):
                    print(f"{player.name} doesn't have enough resources for this counteroffer.")
                    continue

            # Execute the trade
            for resource, amount in final_offer.items():
                player.cards[resource] -= amount
                chosen_player.cards[resource] = chosen_player.cards.get(resource, 0) + amount

            for resource, amount in final_request.items():
                chosen_player.cards[resource] -= amount
                player.cards[resource] = player.cards.get(resource, 0) + amount

            print(f"\nTrade complete! {player.name} gave {final_offer} and received {final_request} from {chosen_player.name}.")
            print(f"{player.name}'s updated cards: {player.cards}")    
        
        

        # Ask it what cards to trade Want -> Receive

        # Go by By turn ask each each player if it wants to accept, reject, or get a counteroffer

        # List the other players responses and allow player 1 decide what he wants to do (accept or reject player i's offer)

        # Ask if it would like to trade again

        # End if it says no

        return
    def StartBuildingPhase(self, player: Player):
        DEV_CARD_COST = {"rock": 1, "wheat": 1, "sheep": 1}
        ROAD_COST = {"wood": 1, "mud": 1}
        SETTLEMENT_COST = {"wood": 1, "mud": 1, "wheat": 1, "sheep": 1}
        CITY_COST = {"rock": 3, "wheat": 2}

        def can_afford(cost: dict):
            return all(player.cards.get(r, 0) >= amt for r, amt in cost.items())

        while True:
            print(f"\n--- {player.name}'s Building Phase ---")
            print(f"Cards: {player.cards}")
            print("What would you like to do?")
            print(f"  [1] Road          (cost: {ROAD_COST})         {'✓' if can_afford(ROAD_COST) else '✗ insufficient resources'}")
            print(f"  [2] Settlement    (cost: {SETTLEMENT_COST})   {'✓' if can_afford(SETTLEMENT_COST) else '✗ insufficient resources'}")
            print(f"  [3] City          (cost: {CITY_COST})         {'✓' if can_afford(CITY_COST) else '✗ insufficient resources'}")
            print(f"  [4] Dev Card      (cost: {DEV_CARD_COST})     {'✓' if can_afford(DEV_CARD_COST) else '✗ insufficient resources'}")
            print(f"  [5] Play Dev Card {'✓' if any(c != 'victory_point' for c in player.dev_cards_inventory) else '✗ no playable cards'}")
            print(f"  [6] Done building")

            choice = input("Enter choice (1-5): ").strip()

            # --- Build Road ---
            if choice == "1":
                if not can_afford(ROAD_COST):
                    print("You don't have enough resources to build a road.")
                    continue
                if player.roads_inventory == 0:
                    print("You have no roads left in your inventory.")
                    continue

                try:
                    start = ast.literal_eval(input("Enter starting node as (tile_idx, node_idx): "))
                    end = ast.literal_eval(input("Enter ending node as (tile_idx, node_idx):   "))
                except (ValueError, SyntaxError):
                    print("Invalid input format. Use (tile_idx, node_idx).")
                    continue
                if not self._valid_road(start, end):
                    print("Out of bounds: tile_idx must be 0-18, node_idx must be 0-5.")
                    continue

                result = player.build_road(self.board, start, end)
                print(result)

            # --- Build Settlement ---
            elif choice == "2":
                if not can_afford(SETTLEMENT_COST):
                    print("You don't have enough resources to build a settlement.")
                    continue
                if player.settlements_inventory == 0:
                    print("You have no settlements left in your inventory.")
                    continue

                try:
                    location = ast.literal_eval(input("Enter settlement location as (tile_idx, node_idx): "))
                    tile_idx, node_idx = location
                except (ValueError, SyntaxError, TypeError):
                    print("Invalid input format. Use (tile_idx, node_idx).")
                    continue
                if not self._valid_node(tile_idx, node_idx):
                    print("Out of bounds: tile_idx must be 0-18, node_idx must be 0-5.")
                    continue
                if not self._valid_settle(tile_idx, node_idx, player):
                    print("Settlement must connect to a road")
                    continue
                result = player.build_settlement(self.board, tile_idx, node_idx)
                print(result)

            # --- Build City ---
            elif choice == "3":
                if not can_afford(CITY_COST):
                    print("You don't have enough resources to build a city.")
                    continue
                if player.cities_inventory == 0:
                    print("You have no cities left in your inventory.")
                    continue
                if not player.settlements:
                    print("You need an existing settlement to upgrade to a city.")
                    continue

                print(f"Your settlements: {player.settlements}")
                try:
                    location = ast.literal_eval(input("Enter settlement to upgrade as (tile_idx, node_idx): "))
                    tile_idx, node_idx = location
                except (ValueError, SyntaxError, TypeError):
                    print("Invalid input format. Use (tile_idx, node_idx).")
                    continue
                if not self._valid_node(tile_idx, node_idx):
                    print("Out of bounds: tile_idx must be 0-18, node_idx must be 0-5.")
                    continue

                if (tile_idx, node_idx) not in player.settlements:
                    print("You don't have a settlement at that location.")
                    continue

                result = player.build_city(self.board, tile_idx, node_idx)
                print(result)

            # --- Buy Dev Card ---
            elif choice == "4":
                if not can_afford(DEV_CARD_COST):
                    print("You don't have enough resources to buy a dev card.")
                    continue
                if not self.board.devCards:
                    print("The dev card deck is empty!")
                    continue

                for resource, amount in DEV_CARD_COST.items():
                    player.cards[resource] -= amount

                drawn_card = random.choice(self.board.devCards)
                self.board.devCards.remove(drawn_card)
                player.dev_cards_inventory.append(drawn_card)

                if drawn_card == "VP":
                    player.num_VPs += 1
                    print(f"You drew a Victory Point card! (kept secret) You now have {player.num_VPs} VPs.")
                else:
                    print(f"You drew a '{drawn_card}' dev card!")
            elif choice == "5":
                self.playDev(player)
            # --- Done ---
            elif choice == "6":
                print(f"{player.name} has finished building.")
                break

            else:
                print("Invalid choice. Please enter a number between 1 and 6.")
    def playDev(self, player: Player):
        # Show the player's dev cards
        if not player.dev_cards_inventory:
            print("You have no dev cards to play.")
            return

        # Filter out victory points — they can't be played, they're automatic
        playable_cards = [card for card in player.dev_cards_inventory if card != "victory_point"]

        if not playable_cards:
            print("You have no playable dev cards (victory points are automatic).")
            return

        print(f"\n--- {player.name}'s Dev Cards ---")
        unique_cards = list(set(playable_cards))
        for i, card in enumerate(unique_cards):
            count = playable_cards.count(card)
            print(f"  [{i+1}] {card} (x{count})")
        print(f"  [{len(unique_cards)+1}] Cancel")

        # Ask which one to play
        try:
            choice = int(input("Which card would you like to play? ")) - 1
        except ValueError:
            print("Invalid input.")
            return

        if choice == len(unique_cards):  # Cancel
            print("Cancelled.")
            return

        if choice < 0 or choice >= len(unique_cards):
            print("Invalid choice.")
            return

        chosen_card = unique_cards[choice]
        player.dev_cards_inventory.remove(chosen_card)
        print(f"Playing '{chosen_card}'...")

        # --- Knight ---
        if chosen_card == "Knight":
            print("You played a Knight card! Move the robber.")
            self.StealCard(player)

            # Track largest army
            knight_count = sum(1 for c in player.dev_cards_inventory if c == "knight")
            knight_count += 1  # include the one just played

            if self.largest_army is None:
                if knight_count >= 3:
                    self.largest_army = player.name
                    player.has_largest_army = True
                    player.num_VPs += 2
                    print(f"{player.name} has claimed the Largest Army! (+2 VPs)")
            else:
                current_holder = next(p for p in self.players if p.name == self.largest_army)
                current_holder_count = sum(1 for c in current_holder.dev_cards_inventory if c == "knight") + 1
                if player.name != self.largest_army and knight_count > current_holder_count:
                    # Take largest army away from current holder
                    current_holder.has_largest_army = False
                    current_holder.num_VPs -= 2
                    # Give it to the new player
                    self.largest_army = player.name
                    player.has_largest_army = True
                    player.num_VPs += 2
                    print(f"{player.name} has taken the Largest Army from {current_holder.name}! (+2 VPs)")

        # --- Year of Plenty ---
        elif chosen_card == "YOP":
            print("You played Year of Plenty! Choose 2 resources to take from the bank.")
            all_resources = ["rock", "wood", "wheat", "mud", "sheep"]

            for i in range(2):
                while True:
                    print(f"Available resources: {all_resources}")
                    resource = input(f"Choose resource {i+1}: ").strip().lower()
                    if resource in all_resources:
                        player.addCards(1, resource)
                        print(f"Added 1 {resource} to your hand.")
                        break
                    else:
                        print("Invalid resource. Choose from: rock, wood, wheat, mud, sheep")

        # --- Monopoly ---
        elif chosen_card == "Mono":
            print("You played Monopoly! Choose a resource to steal from all other players.")
            all_resources = ["rock", "wood", "wheat", "mud", "sheep"]
            print(f"Available resources: {all_resources}")

            while True:
                resource = input("Which resource do you want to monopolize? ").strip().lower()
                if resource in all_resources:
                    break
                print("Invalid resource. Choose from: rock, wood, wheat, mud, sheep")

            total_stolen = 0
            for other_player in self.players:
                if other_player.name != player.name:
                    amount = other_player.cards.get(resource, 0)
                    if amount > 0:
                        other_player.cards[resource] = 0
                        player.addCards(amount, resource)
                        total_stolen += amount
                        print(f"  Stole {amount} {resource} from {other_player.name}.")

            print(f"{player.name} stole a total of {total_stolen} {resource}.")

        # --- Road Building ---
        elif chosen_card == "Road Building":
            print("You played Road Building! You may place 2 free roads.")
            for i in range(2):
                if player.roads_inventory == 0:
                    print("You have no roads left in your inventory.")
                    break
                print(f"Place road {i+1} of 2:")
                while True:
                    try:
                        start = ast.literal_eval(input("  Enter starting node as (tile_idx, node_idx): "))
                        end = ast.literal_eval(input("  Enter ending node as   (tile_idx, node_idx): "))
                    except (ValueError, SyntaxError):
                        print("  Invalid input format. Use (tile_idx, node_idx).")
                        continue
                    # Pass setup=True to bypass resource cost since the card covers it
                    result = player.build_road(self.board, start, end, setup=True)
                    print(f"  {result}")
                    if result == "Added the Road":
                        break
        return
    def ControlRobber(self, player: Player):
        print("Current Tile Position of the Robber: " + str(self.board.robber))
        new_idx = int(input(str(player.name) + ": Which Tile would you like to place the robber on?"))
        self.board.robber = new_idx
        return
    def calculateLongestRoad(self):
        
        for player in self.players:
            # Build a subgraph of only this player's roads
            player_edges = [
                (u, v) for u, v, data in self.board.G.edges(data=True)
                if data.get('roadowner') == player.name
            ]
            
            if not player_edges:
                continue
            
            # Build adjacency list from player's edges
            player_graph = nx.Graph()
            player_graph.add_edges_from(player_edges)

            # Longest road uses DFS from every node, tracking visited edges (not nodes)
            # since you can revisit a node but not an edge
            def dfs(node, visited_edges):
                max_length = len(visited_edges)
                for neighbor in player_graph.neighbors(node):
                    edge = (min(id(node), id(neighbor)), max(id(node), id(neighbor)))
                    if edge not in visited_edges:
                        visited_edges.add(edge)
                        length = dfs(neighbor, visited_edges)
                        max_length = max(max_length, length)
                        visited_edges.remove(edge)
                return max_length

            # Try DFS from every node to find the global longest path
            player_longest = 0
            for start_node in player_graph.nodes():
                length = dfs(start_node, set())
                player_longest = max(player_longest, length)

            print(f"{player.name}'s longest road: {player_longest}")

            # Award longest road if >= 5 and longer than current holder
            if player_longest >= 5:
                if self.longest_road is None:
                    self.longest_road = (player.name, player_longest)
                    player.has_longest_road = True
                    player.num_VPs += 2
                    print(f"{player.name} has claimed the Longest Road! (+2 VPs)")
                else:
                    current_holder_name, current_length = self.longest_road
                    if player.name != current_holder_name and player_longest > current_length:
                        # Remove VPs from old holder
                        current_holder = next(p for p in self.players if p.name == current_holder_name)
                        current_holder.has_longest_road = False
                        current_holder.num_VPs -= 2
                        # Give to new holder
                        self.longest_road = (player.name, player_longest)
                        player.has_longest_road = True
                        player.num_VPs += 2
                        print(f"{player.name} has taken the Longest Road from {current_holder_name}! (+2 VPs)")
                    elif player.name == current_holder_name:
                        # Update the length if the current holder extended their road
                        self.longest_road = (player.name, player_longest)


