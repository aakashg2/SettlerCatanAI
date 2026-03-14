from CatanGame.Game import Game
from CatanGame.Board import Board
from CatanGame.Tile import Tile
from CatanGame.Player import Player
from CatanGame.BoardVisualizer import BoardVisualizer
import networkx as nx
import threading

def game_logic(game, viz):
    # resources = ['Rock', 'Sheep', 'Wheat', "Mud", "Wood"]
    # for resource in resources:
    #     for player in game.players:
    #         player.addCards(3, resource)

    viz.request_pause("Board ready — press SPACE to start setup phase")
    game.setupPhase(debug=True, on_update=viz.request_refresh)
    
    while game._check_winner() == False:
        for i, player in enumerate(game.players):
            viz.request_pause("Player " + str(player.name) + ": press SPACE to roll the dice")
            game.rollDice(player)
            viz.request_pause("Player " + str(player.name) + ": press SPACE to start Build/Trading Phase phase")
            game.StartTradingPhase(player)
            game.StartBuildingPhase(player)
            viz.request_refresh()
            if i < len(game.players) - 1:
                viz.request_pause(f"{player.name} done — press SPACE for next player")

    #game.startGame()

def main():
    board = Board()
    #board.debug_nodes()
    game = Game(4, board, 10, 7, debug=True)
    viz = BoardVisualizer(game.board, game.players)
    #viz.draw()
    t = threading.Thread(target=game_logic, args=(game, viz), daemon=True)
    t.start()
    viz.run_loop()  # main thread: keeps pygame alive and responsive

if __name__ == "__main__":
    main()
