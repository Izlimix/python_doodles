#!/usr/bin/env python3
import itertools
import random

# Test of map setup
# TODO: look at python arg parsing module sys.argv or argparse)
# TODO: look at numpy, its sparse matrices and whether it has built-in (efficient) slicing
#  https://numpy.org/devdocs/user/quickstart.html
#  numpy slicing on a dynamically specified axis: https://stackoverflow.com/questions/24398708/slicing-a-numpy-array-along-a-dynamically-specified-axis
# TODO: Consider line-wise mazes instead of block-wise. Blockwise: Every cell is Passable/Impassable, and linked to every adjacent cell. Line-wise: More similar to a graph. Every node is passable, but only linked to certain adjacent nodes (if they're adjacent and not linked, then draw a line/wall instead). This allows "portals" where two non-adjacent nodes can be linked (it's easier to represent weird topologies). But need to consider how to represent it with minimal duplicated info (transition A->B would normally imply B->A). 

if __name__ == "__main__":
    import sys
    print(f"Received {len(sys.argv)-1} non-standard args:")
    for i in range(1, len(sys.argv)):
        print(i, sys.argv[i])

class Maze:
    """An n-dimensional maze"""
    node_types = ["Wall", "Floor", "Flag"]
    
    def __init__(self, mz_map=dict()):
        self.mz_map = mz_map
        
    def rand_cubic_maze(dimensions, size):
        mz_map = dict()
        for cell in itertools.product(range(size), repeat=dimensions):
            mz_map[cell] = random.choice(Maze.node_types)
        return Maze(mz_map)
    
    def rand_cubic_array_maze(dimensions, size):
        pass
        # Maybe numpy ndarray would work?