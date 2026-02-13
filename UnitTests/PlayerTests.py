import unittest
import random
import networkx as nx
import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname("/home/aakashlinux/Desktop/VirtualGame/UnitTests/Tile_Tests.py"), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from CatanGame.Board import Board
from CatanGame.Tile import Tile
from CatanGame.Player import Player
#testboard = Board()
class TestBoardConstruction(unittest.TestCase):
    # board = Board()
    # player1 = Player("Adam", "Red")
    # player2 = Player("Aryan", "Blue")
    # player3 = Player("Pesto", "Green")
    # player1.addCards("Wood")
    # player1.addCards("Mud")
    # player1.addCards("Sheep")
    # player1.addCards("Wheat")

    # player1.addCards("Wood")
    # player1.addCards("Mud")
    # player1.addCards("Sheep")
    # player1.addCards("Wheat")

    # player1.addCards("Wheat")
    # player1.addCards("Wheat")
    # player1.addCards("Rock")
    # player1.addCards("Rock")
    # player1.addCards("Rock")

    # player2.addCards("Wood")
    # player2.addCards("Mud")
    # player2.addCards("Sheep")
    # player2.addCards("Wheat")
    def setUp(self):
        self.board = Board()
        self.player1 = Player("Adam", "Red")
        self.player2 = Player("Aryan", "Blue")
        self.player3 = Player("Pesto", "Green")
        
        # Add cards

        self.player1.addCards(3,"Wood")
        self.player1.addCards(3,"Mud")
        self.player1.addCards(3,"Sheep")
        self.player1.addCards(3,"Wheat")
        self.player2.addCards(3,"Wood")
        self.player2.addCards(3,"Mud")
        self.player2.addCards(3,"Sheep")
        self.player2.addCards(3,"Wheat")

    def testSoloRoad(self):
        print(self.board.nodemap[(4,1)].owner)
        print(self.player1.build_road(self.board, (4,1), (4,0)))
        print(self.board.nodemap[(4,1)].owner)
        assert self.player1.build_road(self.board, (4,1), (4,0)) == "Your road must connect to a road that you own"
        return
    def testSimpleRoad(self):
        self.player1.build_settlement(self.board, 4,1)
        assert self.player1.build_road(self.board, (4,1), (4,0)) == "Added the Road"
        return
    def testTouchTips(self):        
        self.player1.build_settlement(self.board, 4,1)
        self.player2.build_settlement(self.board, 5,1)
        assert self.player2.build_road(self.board, (5,1), (5,2)) == "Added the Road"
        assert self.player1.build_road(self.board, (4,1), (4,0)) == "Added the Road"
        assert self.player1.build_road(self.board, (4,0), (4,5)) == "Added the Road"
        return
    def testroadthroughsettle(self):
        self.player1.build_settlement(self.board, 4, 1)
        self.player1.build_road(self.board, (4,1), (4,0))
        self.player1.build_road(self.board, (4,0), (4,5))
        self.player1.build_settlement(self.board, 4, 5)

        self.player2.build_settlement(self.board,9,5)
        self.player2.build_road(self.board, (9,5), (9,0))
        self.player2.build_road(self.board, (9,0), (9,1))
        assert self.player2.build_road(self.board, (9,1), (9,2)) == "Foreign Settlement is in the way"
        return
    def ValidSettle(self):
        self.player1.build_settlement(self.board, 4, 1)
        self.player1.build_road(self.board, (4,1), (4,0))
        self.player1.build_road(self.board, (4,0), (4,5))
        assert self.player1.build_settlement(self.board, 4, 5) == "Created a Settlement"
        assert self.player2.build_settlement(self.board, 4,2) == 'Invalid Spot'
        assert self.player2.build_settlement(self.board, 5,5) == 'Created a Settlement'
        self.player2.build_road(self.board, (5,5), (5,0))
        self.player2.build_road(self.board, (5,0), (5,1))
        assert self.player2.build_settlement(self.board, 5,1) == 'Created a Settlement'
        return
    def testRobber(self):
        return
    def testDice(self):
        assert self.player1.build_settlement(self.board, 4, 1) == 'Created a Settlement'
        assert self.player1.build_road(self.board, (4,1), (4,0)) == 'Added the Road'
        assert self.player2.build_settlement(self.board, 4, 5) == 'Created a Settlement'
        assert self.player2.build_road(self.board, (4,5), (4,0)) == 'Added the Road'
        tiles_idx_player1 = [0,1,4]
        for tile_idx in tiles_idx_player1:
            number = Board.tiles[tile_idx].number
            resource = Board.tile[tile_idx].resource
            assert (1,resource) in self.player1.dicemap[number]

        tiles_idx_player2 = [4,5,9]
        for tile_idx in tiles_idx_player2:
            number = Board.tiles[tile_idx].number
            resource = Board.tile[tile_idx].resource
            assert (1,resource) in self.player2.dicemap[number]


        return
    def testLongestRoad(self):
        return
    def testLargestArmy(self):
        return
if __name__ == '__main__':
    unittest.main()