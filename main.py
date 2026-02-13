from CatanGame.Game import Game
from CatanGame.Board import Board
from CatanGame.Tile import Tile
from CatanGame.Player import Player
import networkx as nx

def main():
    
    numberNone = []
    resourceNone = []
    board = Board()
    # for i in range(len(board.tiles)):
    #     for j in range(len(board.tiles[i].nodes)):
    #         if None in board.tiles[i].nodes[j].numbers:
    #             numberNone.append((i,j))
    #         if None in board.tiles[i].nodes[j].resources:
    #             resourceNone.append((i,j))
    # print(numberNone)
    # print(resourceNone)
    # node1 = board.nodemap[(0,0)]
    # node2 = board.nodemap[(0,5)]
    # node3 = board.nodemap[(5,0)]
    # for i, tile in enumerate(board.tiles):
    #     print(str(i)+ "," + tile.resource + "," + str(tile.number))
        
    # print(node1.numbers)
    # print(node1.resources)
    # print("---")
    # print(node2.numbers)
    # print(node2.resources)
    # print("---")
    # print(node3.numbers)
    # print(node3.resources)
    game = Game(4, board, 10, 7, debug = True)
    game.setupPhase(debug=True)
    game.rollDice(game.players[0])
    game.rollDice(game.players[1])
    game.rollDice(game.players[2])
    game.rollDice(game.players[3])
    #game.startGame()

    # player1 = Player("Adam", "Red")
    # player2 = Player("Aryan", "Blue")
    # player3 = Player("Pesto", "Green")
        
    # #     # Add cards

    # player1.addCards(3,"Wood")
    # player1.addCards(3,"Mud")
    # player1.addCards(3,"Sheep")
    # player1.addCards(3,"Wheat")
    # player2.addCards(3,"Wood")
    # player2.addCards(3,"Mud")
    # player2.addCards(3,"Sheep")
    # player2.addCards(3,"Wheat")
    # player1.build_settlement(board, 4, 1)
    # player2.build_settlement(board, 4, 5)
    # print(player1.rollmap)

if __name__ == "__main__":
    main()