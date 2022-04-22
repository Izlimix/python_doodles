"""
    Problem statement: https://www.codewars.com/kata/5671d975d81d6c1c87000022
    Solves a skyscraper puzzle of size 4x4, with clues given in clockwise order.

    Recursive brute-force solution based off of sudoku.py solver.
    Note: Can try a more elegant solution that just generates permutations of 1-4 for
      each row of grid, without storing state (no need to explicitly backtrack).
    Note: Can also try validating just the next possible move, rather than the whole grid every time it recurses.
"""
def solve_puzzle(clues):
    sky = Skyscraper(clues)
    return sky.solve()

class Skyscraper:
    def __init__(self, clues, blanksym=None):
        self.clues = clues
        self.blanksym = blanksym
        self.n = len(clues) // 4
        self.grid = [[None for _ in range(self.n)] for _ in range(self.n)]
        self.heights = set(range(1, self.n+1))
        self.symbols = self.heights.union({self.blanksym})

        #self.debug_recurses = 0

    def solve(self):
        sol = self.brute_recursive()
        if sol:
            return tuple(tuple(row) for row in sol)
        else:
            return None

    def brute_recursive(self):
        #self.debug_recurses += 1
        #if (self.debug_recurses % 100 == 0):
        #    print(f"recurses: {self.debug_recurses}")
        #    for row in self.grid:
        #        print("".join(str(c) for c in row))

        #print("----------Recurse:-----------")
        #print(f"grid:")
        #for row in self.grid:
        #    print("".join(str(c) for c in row))

        pos = self._next_blank()
        if not pos:
            # No more blanks, solved.
            return self.grid
        else:
            (x, y) = pos
            possibles = self.heights - self._neighbours(x, y)
            for v in possibles:
                self.grid[x][y] = v
                if self.valid_move(x, y, v):
                    attempt = self.brute_recursive()
                    if attempt:
                        return attempt #Solved
                    else:
                        #print(f"Ran out of options at {x,y}, backtracking...")
                        self.grid[x][y] = self.blanksym
                else:
                    self.grid[x][y] = self.blanksym
            return None

    def valid_move(self, x, y, v):
        #print("--")
        #print(f"is value {v} at {x,y} valid?")
        # Check whether putting v in position (x,y) would violate any rules.
        row = self.grid[x]
        col = self._col(y)

        # Heights: is v's height in range?
        if v not in self.heights:
            #print("Height not in range")
            return False

        # Unique: No two skyscrapers in a row or column may have the same number of floors (except blanksym)
        floors_r = [f for f in row if f is not self.blanksym]
        if len(set(floors_r)) < len(floors_r):
            #print("Row not unique")
            return False
        floors_c = [f for f in col if f is not self.blanksym]
        if len(set(floors_c)) < len(floors_c):
            #print("Column not unique")
            return False

        # Clues:
        (vert_clues, horiz_clues) = self._pair_clues(self.clues, n=self.n)
        #print(f"v_clues: {vert_clues}")
        #print(f"h_clues: {horiz_clues}")
        (v_c1, v_c2) = vert_clues[y]
        (r_c1, r_c2) = horiz_clues[x]
        if not self._check_row(col, v_c1, v_c2):
            #print(f"Failed col clues v(c1, c2) {v_c1, v_c2}")
            #vis_l = self._count_visible(col)
            #vis_r = self._count_visible(col[::-1])
            #print(f"col: {col}")
            #print(f"visible l,r {vis_l, vis_r}")
            return False
        if not self._check_row(row, r_c1, r_c2):
            #print(f"Failed row clues r(c1, c2) {r_c1, r_c2}")
            #vis_l = self._count_visible(row)
            #vis_r = self._count_visible(row[::-1])
            #print(f"row: {row}")
            #print(f"visible l,r {vis_l, vis_r}")
            return False


        return True

    def is_valid(self):
        # Does the incomplete grid violate any rules?
        # The height of the skyscrapers is between 1 and n (or is incomplete)
        if not all(e in self.symbols for row in self.grid for e in row):
            return False

        # No two skyscrapers in a row or column may have the same number of floors (except blanksym)
        for row in self.grid:
            floors = [f for f in row if f is not self.blanksym]
            if len(set(floors)) < len(floors):
                return False
        for c in range(len(self.grid[0])):
            col = self._col(c)
            floors = [f for f in col if f is not self.blanksym]
            if len(set(floors)) < len(floors):
                return False

        # Clues
        (vert_clues, horiz_clues) = self._pair_clues(self.clues, n=self.n)
        for i in range(len(vert_clues)):
            # column clues valid?
            (c1, c2) = vert_clues[i]
            col = self._col(i)
            if not self._check_row(col, c1, c2):
                return False

        for i in range(len(horiz_clues)):
            #row clues valid?
            (c1, c2) = horiz_clues[i]
            row = self.grid[i]
            if not self._check_row(row, c1, c2):
                return False

        return True

    def _neighbours(self, x, y):
        ns = set(self.grid[x])
        ns.update(self._col(y))
        ns.remove(self.blanksym)
        return ns

    def _next_blank(self):
        # Next blank (None) in l-r, top-bottom order
        for x in range(len(self.grid[0])):
            for y in range(len(self.grid)):
                if self.grid[x][y] is self.blanksym:
                    return (x, y)
        return None

    def _col(self, c):
        return [col[c] for col in self.grid]

    def _check_row(self, seq, c1, c2):
        vis_l = self._count_visible(seq)
        vis_r = self._count_visible(seq[::-1])
        if self.blanksym not in seq:
            # If the row is complete, then the clues should be exact (if not 0).
            return ((not c1) or vis_l == c1) and ((not c2) or vis_r == c2)
        else:
            # Incomplete row, just check for "good enough"
            return ((not c1) or vis_l <= c1) and ((not c2) or vis_r <= c2)

    def _count_visible(self, seq):
        # Take values while next value is > the prev highest.
        # Stops if it reaches a blank (since whatever's placed there might block the count later)
        highest = 0
        count = 0
        for v in seq:
            if v is self.blanksym:
                break
            if v > highest:
                highest = v
                count += 1
        return count

    @staticmethod
    def _pair_clues(clues, n=None):
        # Given a list of clues that correspond to cols/rows in clockwise order,
        # for some grid-size n (default: sqrt of len clues)
        if n is None:
            n = len(clues) // 4
        # Returns two lists ([cols], [rows]), where each element is a pair of clues for the same col/row
        cols = list(zip(clues[:n], clues[2*n:3*n][::-1]))
        #rows = list(zip(clues[n:2*n], clues[3*n:][::-1]))
        rows = list(zip(clues[3*n:][::-1], clues[n:2*n]))
        return (cols, rows)
