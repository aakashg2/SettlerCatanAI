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

#testboard = Board()
class TestBoardConstruction(unittest.TestCase):
    #board = Board()
    def setUp(self):
        board = Board()
        return
    def test_nodemapchecker(self):
        # Test connections with Tile 0
        assert self.board.nodemap[(0,0)] is self.board.nodemap[(1,2)]
        assert self.board.nodemap[(0,3)] is self.board.nodemap[(3,1)]
        assert self.board.nodemap[(0,4)] is self.board.nodemap[(3,0)]
        assert self.board.nodemap[(0,4)] is self.board.nodemap[(4,2)]
        assert self.board.nodemap[(0,5)] is self.board.nodemap[(4,1)]
        assert self.board.nodemap[(0,5)] is self.board.nodemap[(1,3)]

        # Test connections with Tile 1
        assert self.board.nodemap[(1,0)] is self.board.nodemap[(2,2)]
        assert self.board.nodemap[(1,2)] is self.board.nodemap[(0,0)]
        assert self.board.nodemap[(1,3)] is self.board.nodemap[(0,5)]
        assert self.board.nodemap[(1,3)] is self.board.nodemap[(4,1)]
        assert self.board.nodemap[(1,4)] is self.board.nodemap[(4,0)]
        assert self.board.nodemap[(1,4)] is self.board.nodemap[(5,2)]
        assert self.board.nodemap[(1,5)] is self.board.nodemap[(2,3)]
        assert self.board.nodemap[(1,5)] is self.board.nodemap[(5,1)]

        # Test connections with Tile 2
        assert self.board.nodemap[(2,2)] is self.board.nodemap[(1,0)]
        assert self.board.nodemap[(2,3)] is self.board.nodemap[(1,5)]
        assert self.board.nodemap[(2,3)] is self.board.nodemap[(5,1)]
        assert self.board.nodemap[(2,4)] is self.board.nodemap[(5,0)]
        assert self.board.nodemap[(2,4)] is self.board.nodemap[(6,2)]
        assert self.board.nodemap[(2,5)] is self.board.nodemap[(6,1)]

        # Test connections with Tile 3
        assert self.board.nodemap[(3,0)] is self.board.nodemap[(0,4)]
        assert self.board.nodemap[(3,0)] is self.board.nodemap[(4,2)]
        assert self.board.nodemap[(3,1)] is self.board.nodemap[(0,3)]
        assert self.board.nodemap[(3,3)] is self.board.nodemap[(7,1)]
        assert self.board.nodemap[(3,4)] is self.board.nodemap[(7,0)]
        assert self.board.nodemap[(3,4)] is self.board.nodemap[(8,2)]
        assert self.board.nodemap[(3,5)] is self.board.nodemap[(4,3)]
        assert self.board.nodemap[(3,5)] is self.board.nodemap[(8,1)]

        # Test connections with Tile 4
        assert self.board.nodemap[(4,0)] is self.board.nodemap[(5,2)]
        assert self.board.nodemap[(4,0)] is self.board.nodemap[(1,4)]
        assert self.board.nodemap[(4,1)] is self.board.nodemap[(1,3)]
        assert self.board.nodemap[(4,1)] is self.board.nodemap[(0,5)]
        assert self.board.nodemap[(4,2)] is self.board.nodemap[(0,4)]
        assert self.board.nodemap[(4,2)] is self.board.nodemap[(3,0)]
        assert self.board.nodemap[(4,3)] is self.board.nodemap[(3,5)]
        assert self.board.nodemap[(4,3)] is self.board.nodemap[(8,1)]
        assert self.board.nodemap[(4,4)] is self.board.nodemap[(9,2)]
        assert self.board.nodemap[(4,4)] is self.board.nodemap[(8,0)]
        assert self.board.nodemap[(4,5)] is self.board.nodemap[(5,3)]
        assert self.board.nodemap[(4,5)] is self.board.nodemap[(9,1)]

        # Test connections with Tile 5
        assert self.board.nodemap[(5,0)] is self.board.nodemap[(2,4)]
        assert self.board.nodemap[(5,0)] is self.board.nodemap[(6,2)]
        assert self.board.nodemap[(5,1)] is self.board.nodemap[(2,3)]
        assert self.board.nodemap[(5,1)] is self.board.nodemap[(1,5)]
        assert self.board.nodemap[(5,2)] is self.board.nodemap[(1,4)]
        assert self.board.nodemap[(5,2)] is self.board.nodemap[(4,0)]
        assert self.board.nodemap[(5,3)] is self.board.nodemap[(4,5)]
        assert self.board.nodemap[(5,3)] is self.board.nodemap[(9,1)]
        assert self.board.nodemap[(5,4)] is self.board.nodemap[(9,0)]
        assert self.board.nodemap[(5,4)] is self.board.nodemap[(10,2)]
        assert self.board.nodemap[(5,5)] is self.board.nodemap[(10,1)]
        assert self.board.nodemap[(5,5)] is self.board.nodemap[(6,3)]

        # Test connections with Tile 6
        assert self.board.nodemap[(6,1)] is self.board.nodemap[(2,5)]
        assert self.board.nodemap[(6,2)] is self.board.nodemap[(2,4)]
        assert self.board.nodemap[(6,2)] is self.board.nodemap[(5,0)]
        assert self.board.nodemap[(6,3)] is self.board.nodemap[(5,5)]
        assert self.board.nodemap[(6,3)] is self.board.nodemap[(10,1)]
        assert self.board.nodemap[(6,4)] is self.board.nodemap[(11,2)]
        assert self.board.nodemap[(6,4)] is self.board.nodemap[(10,0)]
        assert self.board.nodemap[(6,5)] is self.board.nodemap[(11,1)]

        # Test connections with Tile 7
        assert self.board.nodemap[(7,0)] is self.board.nodemap[(8,2)]
        assert self.board.nodemap[(7,0)] is self.board.nodemap[(3,4)]
        assert self.board.nodemap[(7,1)] is self.board.nodemap[(3,3)]
        assert self.board.nodemap[(7,4)] is self.board.nodemap[(12,2)]
        assert self.board.nodemap[(7,5)] is self.board.nodemap[(8,3)]
        assert self.board.nodemap[(7,5)] is self.board.nodemap[(12,1)]

        # Test connections with Tile 8
        assert self.board.nodemap[(8,0)] is self.board.nodemap[(9,2)]
        assert self.board.nodemap[(8,0)] is self.board.nodemap[(4,4)]
        assert self.board.nodemap[(8,1)] is self.board.nodemap[(4,3)]
        assert self.board.nodemap[(8,1)] is self.board.nodemap[(3,5)]
        assert self.board.nodemap[(8,2)] is self.board.nodemap[(3,4)]
        assert self.board.nodemap[(8,2)] is self.board.nodemap[(7,0)]
        assert self.board.nodemap[(8,3)] is self.board.nodemap[(12,1)]
        assert self.board.nodemap[(8,3)] is self.board.nodemap[(7,5)]
        assert self.board.nodemap[(8,4)] is self.board.nodemap[(13,2)]
        assert self.board.nodemap[(8,4)] is self.board.nodemap[(12,0)]
        assert self.board.nodemap[(8,5)] is self.board.nodemap[(9,3)]
        assert self.board.nodemap[(8,5)] is self.board.nodemap[(13,1)]



        # Test connections with Tile 18
        assert self.board.nodemap[(18,0)] is self.board.nodemap[(15,4)]
        assert self.board.nodemap[(18,1)] is self.board.nodemap[(15,3)]
        assert self.board.nodemap[(18,1)] is self.board.nodemap[(14,5)]
        assert self.board.nodemap[(18,2)] is self.board.nodemap[(14,4)]
        assert self.board.nodemap[(18,2)] is self.board.nodemap[(17,0)]
        assert self.board.nodemap[(18,3)] is self.board.nodemap[(17,5)]
        return

    def test_Tileindexchecker(self):
        # Test connections with Tile 0
        assert self.board.tiles[0].nodes[0] is self.board.tiles[1].nodes[2]
        assert self.board.tiles[0].nodes[3] is self.board.tiles[3].nodes[1]
        assert self.board.tiles[0].nodes[4] is self.board.tiles[3].nodes[0]
        assert self.board.tiles[0].nodes[4] is self.board.tiles[4].nodes[2]
        assert self.board.tiles[0].nodes[5] is self.board.tiles[4].nodes[1]
        assert self.board.tiles[0].nodes[5] is self.board.tiles[1].nodes[3]

        # Test connections with Tile 1
        assert self.board.tiles[1].nodes[0] is self.board.tiles[2].nodes[2]
        assert self.board.tiles[1].nodes[2] is self.board.tiles[0].nodes[0]
        assert self.board.tiles[1].nodes[3] is self.board.tiles[0].nodes[5]
        assert self.board.tiles[1].nodes[3] is self.board.tiles[4].nodes[1]
        assert self.board.tiles[1].nodes[4] is self.board.tiles[4].nodes[0]
        assert self.board.tiles[1].nodes[4] is self.board.tiles[5].nodes[2]
        assert self.board.tiles[1].nodes[5] is self.board.tiles[2].nodes[3]
        assert self.board.tiles[1].nodes[5] is self.board.tiles[5].nodes[1]

        # Test connections with Tile 2
        assert self.board.tiles[2].nodes[2] is self.board.tiles[1].nodes[0]
        assert self.board.tiles[2].nodes[3] is self.board.tiles[1].nodes[5]
        assert self.board.tiles[2].nodes[3] is self.board.tiles[5].nodes[1]
        assert self.board.tiles[2].nodes[4] is self.board.tiles[5].nodes[0]
        assert self.board.tiles[2].nodes[4] is self.board.tiles[6].nodes[2]
        assert self.board.tiles[2].nodes[5] is self.board.tiles[6].nodes[1]

        # Test connections with Tile 3
        assert self.board.tiles[3].nodes[0] is self.board.tiles[0].nodes[4]
        assert self.board.tiles[3].nodes[0] is self.board.tiles[4].nodes[2]
        assert self.board.tiles[3].nodes[1] is self.board.tiles[0].nodes[3]
        assert self.board.tiles[3].nodes[3] is self.board.tiles[7].nodes[1]
        assert self.board.tiles[3].nodes[4] is self.board.tiles[7].nodes[0]
        assert self.board.tiles[3].nodes[4] is self.board.tiles[8].nodes[2]
        assert self.board.tiles[3].nodes[5] is self.board.tiles[4].nodes[3]
        assert self.board.tiles[3].nodes[5] is self.board.tiles[8].nodes[1]

        # Test connections with Tile 4
        assert self.board.tiles[4].nodes[0] is self.board.tiles[5].nodes[2]
        assert self.board.tiles[4].nodes[0] is self.board.tiles[1].nodes[4]
        assert self.board.tiles[4].nodes[1] is self.board.tiles[1].nodes[3]
        assert self.board.tiles[4].nodes[1] is self.board.tiles[0].nodes[5]
        assert self.board.tiles[4].nodes[2] is self.board.tiles[0].nodes[4]
        assert self.board.tiles[4].nodes[2] is self.board.tiles[3].nodes[0]
        assert self.board.tiles[4].nodes[3] is self.board.tiles[3].nodes[5]
        assert self.board.tiles[4].nodes[3] is self.board.tiles[8].nodes[1]
        assert self.board.tiles[4].nodes[4] is self.board.tiles[9].nodes[2]
        assert self.board.tiles[4].nodes[4] is self.board.tiles[8].nodes[0]
        assert self.board.tiles[4].nodes[5] is self.board.tiles[5].nodes[3]
        assert self.board.tiles[4].nodes[5] is self.board.tiles[9].nodes[1]

        # Test connections with Tile 5
        assert self.board.tiles[5].nodes[0] is self.board.tiles[2].nodes[4]
        assert self.board.tiles[5].nodes[0] is self.board.tiles[6].nodes[2]
        assert self.board.tiles[5].nodes[1] is self.board.tiles[2].nodes[3]
        assert self.board.tiles[5].nodes[1] is self.board.tiles[1].nodes[5]
        assert self.board.tiles[5].nodes[2] is self.board.tiles[1].nodes[4]
        assert self.board.tiles[5].nodes[2] is self.board.tiles[4].nodes[0]
        assert self.board.tiles[5].nodes[3] is self.board.tiles[4].nodes[5]
        assert self.board.tiles[5].nodes[3] is self.board.tiles[9].nodes[1]
        assert self.board.tiles[5].nodes[4] is self.board.tiles[9].nodes[0]
        assert self.board.tiles[5].nodes[4] is self.board.tiles[10].nodes[2]
        assert self.board.tiles[5].nodes[5] is self.board.tiles[10].nodes[1]
        assert self.board.tiles[5].nodes[5] is self.board.tiles[6].nodes[3]

        # Test connections with Tile 6
        assert self.board.tiles[6].nodes[1] is self.board.tiles[2].nodes[5]
        assert self.board.tiles[6].nodes[2] is self.board.tiles[2].nodes[4]
        assert self.board.tiles[6].nodes[2] is self.board.tiles[5].nodes[0]
        assert self.board.tiles[6].nodes[3] is self.board.tiles[5].nodes[5]
        assert self.board.tiles[6].nodes[3] is self.board.tiles[10].nodes[1]
        assert self.board.tiles[6].nodes[4] is self.board.tiles[11].nodes[2]
        assert self.board.tiles[6].nodes[4] is self.board.tiles[10].nodes[0]
        assert self.board.tiles[6].nodes[5] is self.board.tiles[11].nodes[1]

        # Test connections with Tile 7
        assert self.board.tiles[7].nodes[0] is self.board.tiles[8].nodes[2]
        assert self.board.tiles[7].nodes[0] is self.board.tiles[3].nodes[4]
        assert self.board.tiles[7].nodes[1] is self.board.tiles[3].nodes[3]
        assert self.board.tiles[7].nodes[4] is self.board.tiles[12].nodes[2]
        assert self.board.tiles[7].nodes[5] is self.board.tiles[8].nodes[3]
        assert self.board.tiles[7].nodes[5] is self.board.tiles[12].nodes[1]

        # Test connections with Tile 8
        assert self.board.tiles[8].nodes[0] is self.board.tiles[9].nodes[2]
        assert self.board.tiles[8].nodes[0] is self.board.tiles[4].nodes[4]
        assert self.board.tiles[8].nodes[1] is self.board.tiles[4].nodes[3]
        assert self.board.tiles[8].nodes[1] is self.board.tiles[3].nodes[5]
        assert self.board.tiles[8].nodes[2] is self.board.tiles[3].nodes[4]
        assert self.board.tiles[8].nodes[2] is self.board.tiles[7].nodes[0]
        assert self.board.tiles[8].nodes[3] is self.board.tiles[12].nodes[1]
        assert self.board.tiles[8].nodes[3] is self.board.tiles[7].nodes[5]
        assert self.board.tiles[8].nodes[4] is self.board.tiles[13].nodes[2]
        assert self.board.tiles[8].nodes[4] is self.board.tiles[12].nodes[0]
        assert self.board.tiles[8].nodes[5] is self.board.tiles[9].nodes[3]
        assert self.board.tiles[8].nodes[5] is self.board.tiles[13].nodes[1]

        # Test connections with Tile 18
        assert self.board.tiles[18].nodes[0] is self.board.tiles[15].nodes[4]
        assert self.board.tiles[18].nodes[1] is self.board.tiles[15].nodes[3]
        assert self.board.tiles[18].nodes[1] is self.board.tiles[14].nodes[5]
        assert self.board.tiles[18].nodes[2] is self.board.tiles[14].nodes[4]
        assert self.board.tiles[18].nodes[2] is self.board.tiles[17].nodes[0]
        assert self.board.tiles[18].nodes[3] is self.board.tiles[17].nodes[5]
        return

if __name__ == '__main__':
    unittest.main()