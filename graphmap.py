#!/usr/bin/env python3

# A directed graph stored as a collection of edges between vertices
# Stored as a map (dict) from start-node to a list of neighbouring nodes.
# Start-node and the neighbouring nodes can be of any type really, as long as they're hashable.

# This edge-graph form can be translated into other representations for viewing, e.g. grid-form.
# Also add some way to "import/parse" other representations into one of these dicts.

# Then, add pathfinding on a graph!
# Can include a demo mode that generates each intermediate path that's considered while searching, the last yielded being either the complete valid path, or the empty path if no route exists.

# Flood-fill helper to find all reachable nodes (over any number of hops) from A?

import math
import itertools

class Graph:
    
    def __init__(self, edges=dict()):
        self.edges = edges
        
    def nodes(self):
        # Note: Doesn't catch nodes that are reachable but have no entry in the edges table.
        return self.edges.keys()
    
    def all_nodes(self):
        return set(self.edges.keys()).union(*self.edges.values())
        
    def neighbours(self, node):
        return self.edges.get(node, [])
    
    def isolated_nodes(self):
        # Doesn't catch nodes which can only go to themselves
        return [node for (node, neighbours) in self.edges.items() if not neighbours]
    
    def loop_nodes(self):
        """Returns a list of the nodes that have themselves as a neighbour."""
        return [node for (node, neighbours) in self.edges.items() if node in neighbours]
    
    def is_bidirectional(self):
        """Is this directed graph a bidirectional one? 
        Bidirectional: For every edge AB, there's a corresponding edge BA.
        Or: Every node is a neighbour of each of its neighbours."""
        return all(node in self.neighbours(neighbour) for node in self.edges.keys() for neighbour in self.neighbours(node))
    
    def valid_path(self, path):
        """Checks that each node in the path is a neighbour of the previous node."""
        return all(end in self.neighbours(start) for (start, end) in zip(path, path[1:]))
    
    def show_ls(self):
        print("Node: Neighbours")
        for (node, neighbours) in self.edges.items():
            print(f"{node}: {neighbours}")
            
    def grid_to_graph(grid):
        """Construct a graph from a 2D-grid (indexed grid[y][x]), with edges between adjacent neighbours.
        Assumes Truthy cells are passable nodes and Falsey cells are walls."""
        g = dict()
        max_rows = len(grid)
        max_cols = len(grid[0])
        for y in range(max_rows):
            for x in range(max_cols):
                # For each cell, if it's not a wall, try and add its neighbours if they're in bounds and they aren't walls
                g[(x, y)] = [(a, b) for (a, b) in Helpers.gen_neighbour_coords((x, y)) if grid[y][x] and Helpers.in_bounds(a, 0, max_cols) and Helpers.in_bounds(b, 0, max_rows) and grid[b][a]]
        return Graph(g)
    
class Weighted_graph(Graph):
    #Todo~
    #  Considering that edges need to have weights associated with them, edge-dict will need to be shaped sth like
    #    {A: [(neighbour, weight)] }
    #    and the neighbour function and weight-functions will need to unpack and repack it as needed.
    def __init__(self, edges=dict()):
        #todo~
        super().__init__(self, edges)
    
class Node():
    #Todo~
    def __init__(self):
        pass
    
    
class Pathfinding:
    
    def iterative_dfs(graph, start, end):
        """Find the shortest path from start to end by repeatedly running depth-first search with iteratively higher depths."""
        # Todo: flood-fill to find max search size?
        if end not in graph.all_nodes(): return []
        
        for d in range(len(graph.nodes())):
            attempt = Pathfinding.depth_first_search(graph, start, end, d)
            if attempt:
                return attempt
        return []
            
    
    def depth_first_search(graph, start, end, depth):
        """Try to get from start to end on the provided graph with a non-repeating path that's no longer than the max depth.
        Depth-first tries to complete the path it's on where possible, backtracking when it runs out of options or depth."""
        return Pathfinding._dfs(graph, [start], end, depth)
        
    def _dfs(graph, path, end, depth):
        if depth < 0:
            # Something's gone wrong, we've already run out of depth.
            return []
        elif path and path[-1] == end:
            # Found the destination!
            return path
        elif depth == 0:
            # We ran out of depth and couldn't find a path.
            return []
        else:
            # Recursively try to dfs from each new neighbour of the last node we visited.
            if not path:
                return [] # Something's gone wrong, our path started empty.
            
            for neighbour in graph.neighbours(path[-1]):
                if neighbour not in path:
                    p = path.copy()
                    p.append(neighbour)
                    attempt = Pathfinding._dfs(graph, p, end, depth - 1)
                    if attempt:
                        return attempt
                    
            return [] # Couldn't find a path
        
    def breadth_first_search(graph, start, end):
        # for each node, store the previous node you took to get there (to form the path at the end)
        seen = {start: None}
        frontier = {start}
        
        if start == end and start in graph.nodes():
            return [start]
        
        while frontier:
            tmp = set()
            for node in frontier:
                #Add each new neighbour of the border nodes
                for neighbour in graph.neighbours(node):
                    if neighbour == end:
                        # We found a path! Trace the path back to start and return it
                        path = [neighbour, node]
                        prev = seen.get(node, None)
                        while prev:
                            path.append(prev)
                            prev = seen.get(prev, None)
                        return path[::-1]
                    elif neighbour not in seen:
                        # New node, add to frontier
                        tmp.add(neighbour)
                        seen[neighbour] = node
            frontier = tmp
        
        return [] # Couldn't find a path
        
    def flood_fill(graph, start):
        # Returns a set of all the reachable nodes from the start node apart from itself, using any number of steps.
        reachable = set()
        new_nodes = set()
        reachable.add(start)
        new_nodes.add(start)
        while new_nodes:
            tmp = set()
            for node in new_nodes:
                for neighbour in graph.neighbours(node):
                    if neighbour not in reachable:
                        tmp.add(neighbour)
                        reachable.add(neighbour)
            new_nodes = tmp
        reachable.remove(start)
        return reachable
        
    
class Demo:
    
    def demo_graph_1():
        # A 5x5 non-wrapping grid, where adjacent nodes have edges.
        return Graph(Demo.simple_graph(5, 5))
    
    def demo_graph_2():
        # An 8x8 wrapping (torus-shaped) grid.
        return Graph(Demo.simple_graph(8, 8, x_wrap=True, y_wrap=True))
    
    def demo_diag_1():
        # A 5x8 non-wrapping grid that's connected on both diagonals and grid lines.
        return Graph(Demo.kings_graph(5, 8))
    
    def demo_walled_1():
        # A 5x5 non-wrapping grid with a wall down the middle (x=2)
        return Graph.grid_to_graph([[x != 2 for x in range(5)] for _ in range(5)])
    
    def simple_graph(cols, rows, *, x_wrap = False, y_wrap = False):
        # A helper function that returns a dict containing the edges in a simply-connected 2d-grid (that can then be constructed into a Graph)
        # Set x_wrap and y_wrap to True for a Torus!
        
        g = dict()
        for x in range(cols):
            for y in range(rows):
                # Adjacent neighbours
                neighbours = [(a, b) for (a, b) in Helpers.gen_neighbour_coords((x, y)) if Helpers.in_bounds(a, 0, cols) and Helpers.in_bounds(b, 0, rows)]
                
                # Wrapping
                col_lim = cols - 1
                row_lim = rows - 1
                # If we wrap on x, then on a 5-wide grid (0,1) is adjacent to (4,1) 
                if x_wrap:
                    if x == 0:
                        neighbours.append((col_lim, y))
                    elif x == col_lim:
                        neighbours.append((0, y))
                
                # If we wrap on y, then on a 5-tall grid (1,0) is adjacent to (1,4)
                if y_wrap:
                    if y == 0:
                        neighbours.append((x, row_lim))
                    elif y == row_lim:
                        neighbours.append((x, 0))
                
                g[(x, y)] = neighbours
        return g
    
    def kings_graph(cols, rows):
        # A cols x rows grid that's also diagonally-connected.
        # https://en.wikipedia.org/wiki/King%27s_graph
        g = dict()
        for x in range(cols):
            for y in range(rows):
                # Adj + Diag neighbours
                neighbours = [(a, b) for (a, b) in Helpers.gen_all_neighbour_coords((x, y)) if Helpers.in_bounds(a, 0, cols) and Helpers.in_bounds(b, 0, rows)]
                
                g[(x, y)] = neighbours
        return g
        
        
    
class Helpers:
    """A collection of static helpers for coordinates and graphs, grouped here for organisational purposes."""
    
    @staticmethod
    def gen_neighbour_offsets(dimensions):
        """Generates the coordinate offsets of the directly-adjacent nodes in n-dimensions."""
        for i in range(dimensions):
            # Directly adjacent nodes only differ by +1/-1 on exactly one axis
            for v in (-1, 1):
                offsets = [0] * dimensions
                offsets[i] = v
                yield offsets
    
    @staticmethod
    def gen_neighbour_coords(node):
        """Given a node of the form (x, y, z, ...), generates the coordinates of directly-adjacent neighbouring nodes on an any-dimensional grid."""
        return (tuple(a + a0 for (a, a0) in zip(node, offsets)) for offsets in Helpers.gen_neighbour_offsets(len(node)))
    
    @staticmethod
    def gen_diag_coords(node):
        """Given a node of the form (x, y, z, ...), generates the coordinates of diagonal neighouring nodes."""
        return (tuple(a + a0 for (a, a0) in zip(node, offsets)) for offsets in filter(Helpers._is_diag_offset, itertools.product((1, 0, -1), repeat=len(node))))
    
    @staticmethod
    def _is_diag_offset(offsets):
        return sum(1 for _ in filter(None, offsets)) > 1
    
    @staticmethod
    def gen_all_neighbour_coords(node):
        """Given a node of the form (x, y, z, ...), generates the coordinates of directly-adjacent neighbouring nodes and diagonal neighbouring nodes on an any-dimensional grid."""
        # Generate all combinations of offset (+1,0,-1) for each of the axes and apply, except for all (0)s
        all_offsets = filter(any, itertools.product((1, 0, -1), repeat=len(node)))
        return (tuple(a + a0 for (a, a0) in zip(node, offsets)) for offsets in all_offsets)
    
    @staticmethod
    def in_bounds(n, lower, upper):
        """Is n between lower (inclusive) and upper (exclusive)?"""
        return lower <= n and n < upper
    
    @staticmethod
    def _coord_offsets(node1, node2):
        """How far on each axis is node2 from node1? Placewise subtraction between two tuples."""
        return tuple(a1 - a2 for (a1, a2) in zip(node1, node2))
    
    @staticmethod
    def _coord_differences(node1, node2):
        """What's the (absolute) difference between node1 and node2 on each axis?"""
        return tuple(abs(a1 - a2) for (a1, a2) in zip(node1, node2))
    
    @staticmethod
    def distance_manhattan(node1, node2):
        """Returns the manhattan distance between two nodes (the distance travelling only along the gridlines).
        Also known as rectilinear distance, taxicab distance, and city block distance."""
        return sum(Helpers._coord_differences(node1, node2))
    
    @staticmethod
    def distance_straightline(node1, node2):
        """Returns the straight-line distance between two nodes using Pythagoras's theorem."""
        return math.sqrt(sum(pow(d, 2) for d in Helpers._coord_offsets(node1, node2)))
    
    @staticmethod
    def distance_chebyshev(node1, node2):
        """Returns the Chebyshev distance between two nodes.
        In this model, a 1-square diagonal movement across multiple axes has the same length as a 1-square movement along only one axis.
        https://en.wikipedia.org/wiki/Chebyshev_distance
        """
        return max(Helpers._coord_differences(node1, node2))
    
    @staticmethod
    def distance_lp_norm(node1, node2, p):
        """Returns the Lp-norm of the distance between two nodes (in finite dimensions).
        For the L-infinity-norm, see Chebyshev distance.
        https://en.wikipedia.org/wiki/Lp_space
        """
        return Helpers.p_norm(Helpers._coord_offsets(node1, node2), p)
    
    @staticmethod
    def p_norm(vector, p):
        """The p-norm in finite dimensions of the given vector."""
        return math.pow(sum(math.pow(abs(a), p) for a in vector), 1/p)
    